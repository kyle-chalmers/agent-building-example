"""Patent Intelligence Agent tools.

This module exports the public API for patent search, Snowflake queries,
and analysis workflow functions.
"""

from tools.patent_search import (
    search_by_assignee,
    search_by_title,
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

# ASSA ABLOY competitors for quick reference
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
    # Constants
    "COMPETITORS",
    "TECHNOLOGIES",
]
