"""Tests for patent intelligence tools."""
import pytest
from unittest.mock import patch, MagicMock


def test_format_patent_for_storage():
    """Test patent data formatting from Google Patents response."""
    from tools import format_patent_for_storage

    # Mock Google Patents API response
    google_patent = {
        "publication_number": "US9792747B2",
        "title": " Smart Lock System ",
        "snippet": "An access control device that&hellip;",
        "assignee": "<b>Allegion</b>, Inc.",
        "inventor": "John Smith",
        "filing_date": "2024-01-15",
        "grant_date": "2024-06-01",
    }

    result = format_patent_for_storage(google_patent)

    assert result["patent_number"] == "US9792747B2"
    assert result["title"] == "Smart Lock System"
    assert result["assignee"] == "Allegion, Inc."
    assert result["filing_date"] == "2024-01-15"
    assert "..." in result["abstract"]  # &hellip; replaced


def test_build_snowflake_query_assignee():
    """Test Snowflake query generation for assignee search."""
    from tools import build_snowflake_query

    query = build_snowflake_query("assignee", "Allegion", 10)

    assert "ILIKE '%Allegion%'" in query
    assert "LIMIT 10" in query
    assert "ORDER BY filing_date DESC" in query


def test_build_snowflake_query_title():
    """Test Snowflake query generation for title search."""
    from tools import build_snowflake_query

    query = build_snowflake_query("title", "smart lock", 20)

    assert "ILIKE '%smart lock%'" in query
    assert "LIMIT 20" in query


def test_is_cache_stale():
    """Test cache staleness check."""
    from datetime import datetime, timedelta
    from tools import is_cache_stale

    # None should be stale
    assert is_cache_stale(None) is True

    # Recent should not be stale
    recent = datetime.now() - timedelta(days=1)
    assert is_cache_stale(recent) is False

    # Old should be stale
    old = datetime.now() - timedelta(days=30)
    assert is_cache_stale(old) is True


def test_generate_report_markdown():
    """Test markdown report generation."""
    from tools import generate_report_markdown

    patents = [
        {
            "patent_number": "US123456",
            "title": "Test Patent",
            "assignee": "Test Corp",
            "filing_date": "2024-01-01",
            "abstract": "Test abstract",
        }
    ]

    report = generate_report_markdown("Test Report", patents)

    assert "# Patent Report: Test Report" in report
    assert "Total patents found: 1" in report
    assert "Test Patent" in report
    assert "Test Corp" in report


def test_competitors_list():
    """Test that competitors list is populated."""
    from tools import COMPETITORS

    assert len(COMPETITORS) > 0
    assert "Allegion" in COMPETITORS


def test_technologies_list():
    """Test that technologies list is populated."""
    from tools import TECHNOLOGIES

    assert len(TECHNOLOGIES) > 0
    assert any("lock" in t for t in TECHNOLOGIES)


def test_build_upsert_query():
    """Test Snowflake MERGE query generation."""
    from tools import build_upsert_query

    patent_data = {
        "patent_number": "US123456",
        "title": "Test Patent",
        "abstract": "Test abstract",
        "assignee": "Test Corp",
        "inventors": ["John Doe"],
        "filing_date": "2024-01-01",
        "grant_date": "2024-06-01",
        "cpc_codes": [],
    }

    query = build_upsert_query(patent_data, "test query", "competitor")

    assert "MERGE INTO" in query
    assert "US123456" in query
    assert "Test Patent" in query


def test_get_trends_query():
    """Test trends query generation."""
    from tools import get_trends_query

    # Without filter
    query = get_trends_query(5)
    assert "GROUP BY assignee" in query
    assert "YEAR(filing_date)" in query

    # With filter
    query = get_trends_query(5, "smart lock")
    assert "ILIKE '%smart lock%'" in query


@pytest.mark.integration
def test_search_by_assignee_live():
    """Integration test: actual Google Patents API call."""
    from tools import search_by_assignee

    # This test actually hits the Google Patents API
    results = search_by_assignee("Allegion", limit=2)

    assert len(results) > 0
    assert results[0]["patent_number"] is not None
    assert results[0]["title"] is not None
