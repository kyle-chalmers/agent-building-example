"""Snowflake SQL query builders for patent data.

This module provides functions to generate Snowflake SQL queries for:
- Patent search (by assignee or title)
- Upserting patent records
- Analyzing filing trends
- Cache staleness checking
"""
import json
from datetime import datetime, timedelta
from typing import Optional


# Cache staleness threshold (days)
CACHE_STALE_DAYS = 7


def is_cache_stale(updated_at: Optional[datetime], days: int = CACHE_STALE_DAYS) -> bool:
    """Check if cached data is stale.

    Args:
        updated_at: Timestamp when data was last updated
        days: Number of days after which data is considered stale

    Returns:
        True if data is stale or updated_at is None
    """
    if updated_at is None:
        return True
    threshold = datetime.now() - timedelta(days=days)
    return updated_at < threshold


def build_snowflake_query(
    search_type: str,
    query: str,
    limit: int = 20
) -> str:
    """Build Snowflake SQL query for patent search.

    Args:
        search_type: Either "assignee" or "title"
        query: Search term
        limit: Maximum results to return

    Returns:
        SQL query string
    """
    if search_type == "assignee":
        return f"""
            SELECT * FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS
            WHERE assignee ILIKE '%{query}%'
            ORDER BY filing_date DESC
            LIMIT {limit};
        """
    else:  # title/keyword search
        return f"""
            SELECT * FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS
            WHERE title ILIKE '%{query}%' OR abstract ILIKE '%{query}%'
            ORDER BY filing_date DESC
            LIMIT {limit};
        """


def build_upsert_query(patent_data: dict, search_query: str, category: str) -> str:
    """Build Snowflake MERGE query to upsert patent data.

    Args:
        patent_data: Dictionary with patent fields
        search_query: Original search query used to find this patent
        category: Category label (e.g., "competitor", "technology")

    Returns:
        SQL MERGE statement
    """
    inventors_json = json.dumps(patent_data.get("inventors", []))
    cpc_json = json.dumps(patent_data.get("cpc_codes", []))

    return f"""
        MERGE INTO SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS AS target
        USING (SELECT
            '{patent_data["patent_number"]}' AS patent_number,
            '{patent_data["title"].replace("'", "''")}' AS title,
            '{(patent_data.get("abstract") or "").replace("'", "''")}' AS abstract,
            '{patent_data["assignee"]}' AS assignee,
            PARSE_JSON('{inventors_json}') AS inventors,
            '{patent_data["filing_date"]}' AS filing_date,
            {f"'{patent_data['grant_date']}'" if patent_data.get("grant_date") else "NULL"} AS grant_date,
            PARSE_JSON('{cpc_json}') AS cpc_codes,
            '{search_query}' AS search_query,
            '{category}' AS category
        ) AS source
        ON target.patent_number = source.patent_number
        WHEN MATCHED THEN UPDATE SET
            title = source.title,
            abstract = source.abstract,
            assignee = source.assignee,
            inventors = source.inventors,
            filing_date = source.filing_date,
            grant_date = source.grant_date,
            cpc_codes = source.cpc_codes,
            search_query = source.search_query,
            category = source.category,
            updated_at = CURRENT_TIMESTAMP()
        WHEN NOT MATCHED THEN INSERT (
            patent_number, title, abstract, assignee, inventors,
            filing_date, grant_date, cpc_codes, search_query, category,
            created_at, updated_at
        ) VALUES (
            source.patent_number, source.title, source.abstract, source.assignee,
            source.inventors, source.filing_date, source.grant_date, source.cpc_codes,
            source.search_query, source.category, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()
        );
    """


def get_trends_query(years: int = 5, technology_filter: Optional[str] = None) -> str:
    """Generate Snowflake query for patent filing trends.

    Args:
        years: Number of years to analyze
        technology_filter: Optional technology keyword filter

    Returns:
        SQL query string
    """
    tech_clause = ""
    if technology_filter:
        tech_clause = f"AND (title ILIKE '%{technology_filter}%' OR abstract ILIKE '%{technology_filter}%')"

    return f"""
        SELECT
            assignee,
            YEAR(filing_date) as year,
            COUNT(*) as patent_count
        FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS
        WHERE filing_date >= DATEADD(year, -{years}, CURRENT_DATE())
        {tech_clause}
        GROUP BY assignee, YEAR(filing_date)
        ORDER BY year DESC, patent_count DESC;
    """
