"""Data loading utilities for Snowflake patent cache.

This module provides functions to fetch patents from the USPTO API
and generate SQL statements to load them into Snowflake.
"""
import subprocess
from typing import Optional

from tools.snowflake_queries import build_upsert_query
from tools.patent_search import search_by_assignee, search_by_title


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


def get_create_table_sql() -> str:
    """Get SQL to create the PATENTS table.

    Returns:
        CREATE TABLE SQL statement
    """
    return """
CREATE TABLE IF NOT EXISTS SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS (
    patent_number VARCHAR PRIMARY KEY,
    title VARCHAR,
    abstract TEXT,
    assignee VARCHAR,
    inventors VARIANT,
    filing_date DATE,
    grant_date DATE,
    cpc_codes VARIANT,
    search_query VARCHAR,
    category VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
"""
