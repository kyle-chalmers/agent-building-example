"""Patent data wrapper using USPTO Open Data Portal API.

Primary source: USPTO ODP API (api.uspto.gov) - requires API key
Fallback: Google Patents API (rate-limited, no key required)
Last resort: Sample data for demos

API key should be set in environment variable USPTO_API_KEY or .env file.
"""
import json
import os
import urllib.parse
import urllib.request
from typing import Optional


# USPTO Open Data Portal API
USPTO_ODP_API = "https://api.uspto.gov/api/v1/patent/applications/search"

# Google Patents API (fallback)
GOOGLE_PATENTS_API = "https://patents.google.com/xhr/query"

# Sample data for demo when APIs are unavailable
SAMPLE_PATENTS = {
    "assa abloy": [
        {
            "patent_number": "US20250001234A1",
            "title": "Multi-factor authentication door access control system",
            "abstract": "A door access control system that combines biometric verification with mobile credentials...",
            "assignee": "ASSA ABLOY Global Solutions AB",
            "inventors": ["Erik Lindqvist", "Anna Svensson"],
            "filing_date": "2025-09-03",
            "grant_date": None,
            "cpc_codes": ["E05B47/00", "G07C9/00"],
        },
        {
            "patent_number": "US20250005678A1",
            "title": "Beacon circuit for use with electronic locks",
            "abstract": "An electronic lock system with integrated beacon circuitry for proximity detection...",
            "assignee": "ASSA ABLOY AB",
            "inventors": ["Johan Berg"],
            "filing_date": "2025-08-07",
            "grant_date": None,
            "cpc_codes": ["E05B47/00", "H04W4/80"],
        },
    ],
    "allegion": [
        {
            "patent_number": "US9792747B2",
            "title": "Multifunctional access control device",
            "abstract": "An access control device that at least assists in controlling the ingress/egress through an entryway...",
            "assignee": "Allegion, Inc.",
            "inventors": ["Joseph Wayne Baumgarte"],
            "filing_date": "2015-10-19",
            "grant_date": "2017-10-17",
            "cpc_codes": [],
        },
    ],
    "dormakaba": [
        {
            "patent_number": "US10878656B2",
            "title": "Access control device with biometric verification",
            "abstract": "A door access control system incorporating fingerprint and facial recognition...",
            "assignee": "dormakaba Holding AG",
            "inventors": ["Hans Mueller"],
            "filing_date": "2018-05-10",
            "grant_date": "2020-12-29",
            "cpc_codes": [],
        },
    ],
    "smart lock": [
        {
            "patent_number": "US10789800B2",
            "title": "Smart lock with voice assistant integration",
            "abstract": "A smart lock system that integrates with voice assistants for hands-free operation...",
            "assignee": "August Home, Inc.",
            "inventors": ["Jason Johnson"],
            "filing_date": "2017-09-14",
            "grant_date": "2020-09-29",
            "cpc_codes": [],
        },
    ],
}


def _get_api_key() -> Optional[str]:
    """Get USPTO API key from environment or .env file.

    Returns:
        API key string or None if not found
    """
    # Check environment variable first
    api_key = os.environ.get("USPTO_API_KEY")
    if api_key:
        return api_key

    # Try loading from .env file
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("USPTO_API_KEY="):
                    return line.strip().split("=", 1)[1]

    return None


def search_by_assignee(company: str, limit: int = 50) -> list[dict]:
    """Search patents by assignee/company name.

    Args:
        company: Company name to search for (e.g., "ASSA ABLOY", "Allegion")
        limit: Maximum number of results to return

    Returns:
        List of patent dictionaries
    """
    # Try USPTO ODP API first (primary source)
    results = _search_uspto_odp(company, limit)
    if results:
        return results

    # Fallback to Google Patents
    print(f"[USPTO API unavailable, trying Google Patents for '{company}']")
    query = f"assignee={company}"
    results = _search_google_patents(query, limit)
    if results:
        return results

    # Last resort: sample data for demos
    results = _get_sample_data(company.lower(), limit)
    return results


def search_by_title(keywords: str, limit: int = 50) -> list[dict]:
    """Search patents by title keywords.

    Args:
        keywords: Keywords to search in patent titles (e.g., "smart lock")
        limit: Maximum number of results to return

    Returns:
        List of patent dictionaries
    """
    # Try USPTO ODP API first (primary source)
    results = _search_uspto_odp(keywords, limit)
    if results:
        return results

    # Fallback to Google Patents
    print(f"[USPTO API unavailable, trying Google Patents for '{keywords}']")
    query = f"({keywords})"
    results = _search_google_patents(query, limit)
    if results:
        return results

    # Last resort: sample data for demos
    results = _get_sample_data(keywords.lower(), limit)
    return results


def get_patent(patent_number: str) -> Optional[dict]:
    """Get single patent by publication number.

    Args:
        patent_number: Publication number (e.g., "US9792747B2")

    Returns:
        Patent dictionary or None if not found
    """
    # Try USPTO first
    results = _search_uspto_odp(patent_number, 1)
    if results:
        return results[0]

    # Fallback to Google Patents
    results = _search_google_patents(patent_number, 1)
    return results[0] if results else None


def _search_uspto_odp(query: str, limit: int) -> list[dict]:
    """Search USPTO Open Data Portal API.

    Args:
        query: Search query (company name, keywords, or patent number)
        limit: Maximum results to return

    Returns:
        List of patent dictionaries, empty list on failure
    """
    api_key = _get_api_key()
    if not api_key:
        print("[No USPTO_API_KEY found - set in environment or .env file]")
        return []

    params = {
        "q": query,
        "rows": min(limit, 100),
    }

    url = f"{USPTO_ODP_API}?{urllib.parse.urlencode(params)}"

    headers = {
        "X-API-KEY": api_key,
        "Accept": "application/json",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())

        results = []
        for app in data.get("patentFileWrapperDataBag", []):
            patent = _format_uspto_patent(app)
            if patent:
                results.append(patent)
                if len(results) >= limit:
                    break

        if results:
            print(f"[USPTO ODP: Found {data.get('count', 0)} total, returning {len(results)}]")

        return results

    except urllib.error.HTTPError as e:
        if e.code == 401 or e.code == 403:
            print(f"[USPTO API authentication failed (HTTP {e.code}) - check API key]")
        else:
            print(f"[USPTO API error: HTTP {e.code}]")
        return []
    except Exception as e:
        print(f"[USPTO API error: {e}]")
        return []


def _format_uspto_patent(app: dict) -> Optional[dict]:
    """Convert USPTO ODP result to standardized dict for storage.

    Args:
        app: Application data from USPTO ODP API

    Returns:
        Standardized patent dictionary or None if invalid
    """
    meta = app.get("applicationMetaData", {})
    if not meta:
        return None

    # Extract applicant/assignee
    applicants = meta.get("applicantBag", [])
    assignee = ""
    if applicants:
        assignee = applicants[0].get("applicantNameText", "")

    # Extract inventors
    inventors = []
    for inv in meta.get("inventorBag", []):
        name = inv.get("inventorNameText", "")
        if name:
            inventors.append(name)

    # Format dates (remove time component)
    filing_date = meta.get("filingDate", "")
    if filing_date and "T" in filing_date:
        filing_date = filing_date.split("T")[0]

    # Extract CPC codes if available
    cpc_codes = []
    for cpc in meta.get("cpcClassificationBag", []):
        if isinstance(cpc, dict) and cpc.get("cpcClassificationText"):
            cpc_codes.append(cpc["cpcClassificationText"])
        elif isinstance(cpc, str):
            cpc_codes.append(cpc)

    return {
        "patent_number": meta.get("earliestPublicationNumber", ""),
        "title": meta.get("inventionTitle", ""),
        "abstract": "",  # ODP search doesn't include abstract
        "assignee": assignee,
        "inventors": inventors,
        "filing_date": filing_date,
        "grant_date": None,  # Would need separate lookup
        "cpc_codes": cpc_codes,
        "status_code": meta.get("applicationStatusCode"),
    }


def _get_sample_data(key: str, limit: int) -> list[dict]:
    """Get sample data for demos when APIs are unavailable.

    Args:
        key: Search key (company name or keywords)
        limit: Maximum results

    Returns:
        List of sample patent dictionaries
    """
    for sample_key, patents in SAMPLE_PATENTS.items():
        if sample_key in key or key in sample_key:
            print(f"[Using sample data for '{key}' - APIs unavailable]")
            return patents[:limit]
    return []


def _search_google_patents(query: str, limit: int) -> list[dict]:
    """Search Google Patents API (fallback).

    Args:
        query: Search query string
        limit: Maximum results to return

    Returns:
        List of patent dictionaries
    """
    params = {
        "url": query,
        "num": min(limit, 100),
        "exp": "",
        "output": "json"
    }

    url = f"{GOOGLE_PATENTS_API}?{urllib.parse.urlencode(params)}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://patents.google.com/",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())

        results = []
        clusters = data.get("results", {}).get("cluster", [])
        for cluster in clusters:
            for item in cluster.get("result", []):
                patent = item.get("patent", {})
                results.append(_format_google_patent(patent))
                if len(results) >= limit:
                    return results

        return results

    except urllib.error.HTTPError as e:
        if e.code == 503 or e.code == 429:
            print(f"[Google Patents rate limited (HTTP {e.code})]")
        else:
            print(f"[Google Patents error: HTTP {e.code}]")
        return []
    except Exception as e:
        print(f"[Google Patents error: {e}]")
        return []


def _format_google_patent(patent: dict) -> dict:
    """Convert Google Patents result to standardized dict.

    Args:
        patent: Patent dictionary from Google Patents API

    Returns:
        Standardized patent dictionary
    """
    assignee = patent.get("assignee", "")
    if assignee:
        assignee = assignee.replace("<b>", "").replace("</b>", "")

    return {
        "patent_number": patent.get("publication_number", ""),
        "title": patent.get("title", "").strip(),
        "abstract": patent.get("snippet", "").replace("&hellip;", "..."),
        "assignee": assignee,
        "inventors": [patent.get("inventor", "")] if patent.get("inventor") else [],
        "filing_date": patent.get("filing_date"),
        "grant_date": patent.get("grant_date"),
        "cpc_codes": [],
    }


# Keep old function name for backwards compatibility
def format_patent_for_storage(patent: dict) -> dict:
    """Convert patent result to standardized dict for Snowflake storage.

    Args:
        patent: Patent dictionary from any source

    Returns:
        Dictionary with standardized fields for database storage
    """
    return _format_google_patent(patent)
