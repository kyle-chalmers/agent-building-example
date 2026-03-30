"""Data loading utilities for Snowflake patent cache.

This module provides functions to fetch patents from the USPTO API
and generate SQL statements to load them into Snowflake.
"""
import subprocess
import json
import time
from typing import Optional

from tools.snowflake_queries import build_upsert_query
from tools.patent_search import search_by_assignee, search_by_title, get_patent


def load_competitor_patents(company: str, limit: int = 50, execute: bool = False) -> list[str]:
    """Fetch patents for a company and generate Snowflake upsert SQL.

    Args:
        company: Company name to search for
        limit: Maximum patents to fetch
        execute: If True, execute SQL via snow CLI (requires snow to be configured)

    Returns:
        List of SQL statements generated
    """
    patents = search_by_assignee(company, limit)
    sql_statements = []

    for patent in patents:
        if patent.get("patent_number"):
            sql = build_upsert_query(patent, company, "competitor")
            sql_statements.append(sql)

            if execute:
                _execute_snowflake_sql(sql)

    print(f"[{company}]: Generated {len(sql_statements)} upsert statements")
    return sql_statements


def load_technology_patents(keywords: str, limit: int = 50, execute: bool = False) -> list[str]:
    """Fetch patents by technology keywords and generate Snowflake upsert SQL.

    Args:
        keywords: Technology keywords to search
        limit: Maximum patents to fetch
        execute: If True, execute SQL via snow CLI

    Returns:
        List of SQL statements generated
    """
    patents = search_by_title(keywords, limit)
    sql_statements = []

    for patent in patents:
        if patent.get("patent_number"):
            sql = build_upsert_query(patent, keywords, "technology")
            sql_statements.append(sql)

            if execute:
                _execute_snowflake_sql(sql)

    print(f"[{keywords}]: Generated {len(sql_statements)} upsert statements")
    return sql_statements


def load_all_competitors(limit_per_company: int = 50, execute: bool = False) -> dict[str, int]:
    """Load patents for all tracked competitors.

    Args:
        limit_per_company: Maximum patents per competitor
        execute: If True, execute SQL via snow CLI

    Returns:
        Dictionary mapping company name to number of patents loaded
    """
    from tools import COMPETITORS

    results = {}
    for company in COMPETITORS:
        statements = load_competitor_patents(company, limit_per_company, execute)
        results[company] = len(statements)

    total = sum(results.values())
    print(f"\n[Total]: Generated {total} upsert statements for {len(COMPETITORS)} competitors")
    return results


def load_all_technologies(limit_per_tech: int = 20, execute: bool = False) -> dict[str, int]:
    """Load patents for all tracked technology keywords.

    Args:
        limit_per_tech: Maximum patents per technology
        execute: If True, execute SQL via snow CLI

    Returns:
        Dictionary mapping technology to number of patents loaded
    """
    from tools import TECHNOLOGIES

    results = {}
    for tech in TECHNOLOGIES:
        statements = load_technology_patents(tech, limit_per_tech, execute)
        results[tech] = len(statements)

    total = sum(results.values())
    print(f"\n[Total]: Generated {total} upsert statements for {len(TECHNOLOGIES)} technologies")
    return results


def _execute_snowflake_sql(sql: str) -> Optional[str]:
    """Execute SQL statement via snow CLI.

    Args:
        sql: SQL statement to execute

    Returns:
        Command output or None on failure
    """
    try:
        result = subprocess.run(
            ["snow", "sql", "-q", sql],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            print(f"[Snowflake error]: {result.stderr}")
            return None
        return result.stdout
    except subprocess.TimeoutExpired:
        print("[Snowflake timeout]")
        return None
    except FileNotFoundError:
        print("[snow CLI not found - install with: pip install snowflake-cli]")
        return None


def sync_application_number_from_uspto_metadata(execute: bool = False) -> Optional[str]:
    """Fill empty `application_number` from cached `uspto_metadata` VARIANT.

    USPTO search responses often omit `applicationNumberText` but include
    `applicationConfirmationNumber`. This updates existing rows without
    calling the API again.

    Args:
        execute: If True, run UPDATE via snow CLI.

    Returns:
        snow CLI stdout on success, None on failure or when execute is False.
    """
    sql = """
        UPDATE SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS
        SET application_number = COALESCE(
            NULLIF(TRIM(application_number), ''),
            NULLIF(TRIM(uspto_metadata:applicationNumberText::STRING), ''),
            NULLIF(TRIM(uspto_metadata:applicationConfirmationNumber::STRING), '')
        )
        WHERE uspto_metadata IS NOT NULL
          AND (application_number IS NULL OR TRIM(application_number) = '');
    """
    if not execute:
        return None
    return _execute_snowflake_sql(sql)


def backfill_uspto_metadata(
    batch_size: int = 100,
    max_records: Optional[int] = None,
    execute: bool = False,
    sleep_seconds: float = 1.0,
) -> dict[str, int]:
    """Backfill missing USPTO fields for existing cached patents.

    This process is idempotent: it only targets rows missing enrichable
    USPTO-derived fields (`status_code`, `uspto_metadata`) and uses MERGE
    upserts per record. `application_number` is not used in the filter so
    we do not loop forever when USPTO omits `applicationNumberText` but
    still provides confirmation numbers via normalization.

    Args:
        batch_size: Number of candidate rows to fetch from Snowflake per batch.
        max_records: Optional hard cap on total rows to process.
        execute: If True, execute generated MERGE SQL against Snowflake.
        sleep_seconds: Delay between USPTO requests to respect rate limits.

    Returns:
        Counters for attempted, enriched, skipped, failed.
    """
    if execute:
        sync_application_number_from_uspto_metadata(execute=True)

    counters = {"attempted": 0, "enriched": 0, "skipped": 0, "failed": 0}
    while True:
        select_sql = f"""
            SELECT patent_number, search_query, category
            FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS
            WHERE status_code IS NULL
               OR uspto_metadata IS NULL
            ORDER BY updated_at ASC
            LIMIT {batch_size}
            OFFSET 0;
        """
        rows = _query_snowflake_rows(select_sql)
        if not rows:
            break

        batch_enriched = 0
        for row in rows:
            patent_number = row.get("PATENT_NUMBER") or row.get("patent_number")
            if not patent_number:
                counters["skipped"] += 1
                continue

            if max_records is not None and counters["attempted"] >= max_records:
                return counters

            counters["attempted"] += 1
            enriched = get_patent(patent_number)
            if not enriched:
                counters["failed"] += 1
                continue

            search_query = row.get("SEARCH_QUERY") or row.get("search_query") or "backfill"
            category = row.get("CATEGORY") or row.get("category") or "backfill"
            sql = build_upsert_query(enriched, search_query, category)

            if execute:
                output = _execute_snowflake_sql(sql)
                if output is None:
                    counters["failed"] += 1
                    continue

            counters["enriched"] += 1
            batch_enriched += 1
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)

        if batch_enriched == 0:
            break

    return counters


def _query_snowflake_rows(sql: str) -> list[dict]:
    """Execute a Snowflake query and return parsed JSON rows."""
    try:
        result = subprocess.run(
            ["snow", "sql", "-q", sql, "--format", "json"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            print(f"[Snowflake query error]: {result.stderr}")
            return []
        data = json.loads(result.stdout)
        if isinstance(data, list):
            return data
        return data.get("data", []) if isinstance(data, dict) else []
    except subprocess.TimeoutExpired:
        print("[Snowflake query timeout]")
        return []
    except FileNotFoundError:
        print("[snow CLI not found - install with: pip install snowflake-cli]")
        return []
    except json.JSONDecodeError:
        print("[Snowflake query JSON parse error]")
        return []


def get_create_table_sql() -> str:
    """Get SQL to create the PATENTS table.

    Returns:
        CREATE TABLE SQL statement
    """
    return """
CREATE TABLE IF NOT EXISTS SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS (
    patent_number VARCHAR PRIMARY KEY,
    application_number VARCHAR,
    title VARCHAR,
    abstract TEXT,
    assignee VARCHAR,
    inventors VARIANT,
    filing_date DATE,
    grant_date DATE,
    cpc_codes VARIANT,
    status_code NUMBER,
    uspto_metadata VARIANT,
    search_query VARCHAR,
    category VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
"""
