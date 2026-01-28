"""Patent Intelligence Agent tools.

This module exports the public API for patent search, Snowflake queries,
and analysis workflow functions.
"""

from tools.patent_search import (
    search_by_assignee,
    search_by_title,
    search_by_cpc,
    get_patent,
    format_patent_for_storage,
    SAMPLE_PATENTS,
)

from tools.snowflake_queries import (
    build_snowflake_query,
    build_upsert_query,
    get_trends_query,
    is_cache_stale,
    CACHE_STALE_DAYS,
)

from tools.analysis_workflow import (
    AnalysisWorkflow,
    create_session_dir,
    generate_report_markdown,
)

from tools.data_loader import (
    load_competitor_patents,
    load_technology_patents,
    load_all_competitors,
    load_all_technologies,
    get_create_table_sql,
)

# Competitors for quick reference (configure for your company)
COMPETITORS = [
    "Allegion",
    "Dormakaba",
    "Spectrum Brands",
    "Stanley Black & Decker",
]

# Relevant technology keywords
TECHNOLOGIES = [
    "smart lock",
    "electronic lock",
    "biometric access",
    "RFID access",
    "NFC access",
    "keyless entry",
    "mobile credential",
    "door hardware",
    "access control",
]

__all__ = [
    # Patent search functions
    "search_by_assignee",
    "search_by_title",
    "search_by_cpc",
    "get_patent",
    "format_patent_for_storage",
    "SAMPLE_PATENTS",
    # Snowflake query builders
    "build_snowflake_query",
    "build_upsert_query",
    "get_trends_query",
    "is_cache_stale",
    "CACHE_STALE_DAYS",
    # Analysis workflow
    "AnalysisWorkflow",
    "create_session_dir",
    "generate_report_markdown",
    # Data loader
    "load_competitor_patents",
    "load_technology_patents",
    "load_all_competitors",
    "load_all_technologies",
    "get_create_table_sql",
    # Constants
    "COMPETITORS",
    "TECHNOLOGIES",
]
