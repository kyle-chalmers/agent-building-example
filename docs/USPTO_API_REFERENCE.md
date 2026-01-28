# USPTO Open Data Portal API Reference

## Overview

The USPTO Open Data Portal (ODP) API is the **primary data source** for this Patent Intelligence Agent. It provides real-time access to 12.6M+ US patent applications with current filing status, assignee information, and classification codes.

**Why USPTO ODP is primary:**
- Most current data (updated daily)
- Official source for US patent applications
- Includes pending applications not yet in BigQuery
- Provides application status codes

---

## Authentication

### API Key Setup

The USPTO ODP API requires an API key for all requests.

**Get your key:** https://data.uspto.gov/key/myapikey

**Configuration (in order of precedence):**

1. **Environment variable** (recommended for production):
   ```bash
   export USPTO_API_KEY=your-api-key-here
   ```

2. **`.env` file** (recommended for development):
   ```bash
   # .env
   USPTO_API_KEY=your-api-key-here
   ```

**Verify configuration:**
```bash
python3 -c "from tools.patent_search import _get_api_key; print('OK' if _get_api_key() else 'MISSING')"
```

---

## Endpoints

### Patent Applications Search

**URL:** `https://api.uspto.gov/api/v1/patent/applications/search`

**Method:** GET

**Required Headers:**
| Header | Value |
|--------|-------|
| `X-API-KEY` | Your USPTO API key |
| `Accept` | `application/json` |

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | Search query (see Query Syntax below) |
| `rows` | integer | Number of results (max 100) |
| `start` | integer | Offset for pagination |

**Example Request:**
```bash
curl -X GET "https://api.uspto.gov/api/v1/patent/applications/search?q=Allegion&rows=10" \
  -H "X-API-KEY: your-api-key" \
  -H "Accept: application/json"
```

---

## Search Query Syntax

### CRITICAL: Default OR Behavior

The USPTO API uses **OR matching by default** for multi-word queries. This is the most common source of irrelevant results.

| Query | Actual Behavior | Results | Relevance |
|-------|-----------------|---------|-----------|
| `smart lock` | `smart OR lock` | ~69,000 | ~10% relevant |
| `"smart lock"` | Exact phrase | ~200 | ~100% relevant |
| `smart AND lock` | Both terms required | ~1,500 | ~80% relevant |
| `smart AND lock AND door` | All terms required | ~80 | ~100% relevant |

### Best Practices

#### 1. Quoted Phrases (Recommended)

Wrap multi-word terms in double quotes for exact phrase matching:

```python
# BAD - returns "smart" OR "lock" (69,000+ results)
search_by_title("smart lock")

# GOOD - returns exact phrase "smart lock" (200 results)
search_by_title('"smart lock"')

# GOOD - multiple quoted phrases
search_by_title('"electronic lock" AND "access control"')
```

#### 2. Boolean Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `AND` | All terms required | `electronic AND lock AND door` |
| `OR` | Any term matches | `lock OR latch` |
| `NOT` | Exclude term | `lock NOT automotive` |
| `()` | Grouping | `(lock OR latch) AND electronic` |

**Examples:**
```python
# All terms required
search_by_title('electronic AND lock AND residential')

# Exclude irrelevant domains
search_by_title('lock NOT automotive NOT vehicle NOT aircraft')

# Complex boolean
search_by_title('(smart OR electronic) AND lock AND (door OR entry)')
```

#### 3. CPC Code Searches (Most Precise)

For highest precision, use CPC classification codes instead of keywords:

```python
# Most accurate - uses BigQuery with CPC classification
search_by_cpc("E05B47", min_grant_date="20240101")

# Filter by competitor
search_by_cpc("E05B47", assignee_filter="Allegion")
```

### Query Precision Comparison

| Method | Precision | Speed | Best For |
|--------|-----------|-------|----------|
| `search_by_cpc()` | Highest | Medium | Competitive analysis, technology landscape |
| `search_by_title()` with quotes | High | Fast | Specific phrase searches |
| `search_by_assignee()` | High | Fast | Company-specific searches |
| `search_by_title()` unquoted | Low | Fast | **Avoid** - returns noise |

---

## Response Schema

### Response Structure

```json
{
  "count": 1234,
  "patentFileWrapperDataBag": [
    {
      "applicationMetaData": {
        "applicationNumberText": "17123456",
        "filingDate": "2024-01-15T00:00:00Z",
        "inventionTitle": "Smart Lock with Biometric Authentication",
        "earliestPublicationNumber": "US20240123456A1",
        "applicationStatusCode": 30,
        "applicantBag": [...],
        "inventorBag": [...],
        "cpcClassificationBag": [...]
      }
    }
  ]
}
```

### Standardized Patent Object

The `tools.patent_search` module normalizes USPTO responses to this format:

| Field | Type | Description |
|-------|------|-------------|
| `patent_number` | string | Publication number (e.g., "US20240123456A1") |
| `title` | string | Invention title |
| `abstract` | string | Patent abstract (may be empty from search) |
| `assignee` | string | Current assignee/applicant |
| `inventors` | list[string] | List of inventor names |
| `filing_date` | string | Filing date (YYYY-MM-DD) |
| `grant_date` | string | Grant date if granted (YYYY-MM-DD or null) |
| `cpc_codes` | list[string] | CPC classification codes |
| `status_code` | integer | Application status code |

### Application Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 10 | Pending | Under examination |
| 20 | Allowed | Approved, awaiting issue |
| 30 | Published | Published application |
| 150 | Issued | Granted patent |
| 161 | Abandoned | Application abandoned |

---

## CPC Classification Codes

### Relevant Codes for Lock/Access Control

| Code | Description |
|------|-------------|
| **E05B** | Locks; accessories therefor; handcuffs |
| E05B47 | Operating or controlling locks by electric or magnetic means |
| E05B49 | Electric permutation locks; circuits therefor |
| E05B65 | Locks for special use (vehicles, furniture, etc.) |
| **E05C** | Bolts; fastening devices for doors/windows |
| **E05F** | Closers, openers, checks for doors/windows |
| **G07C9** | Access control systems |
| G07C9/00 | Individual registration on entry or exit |
| G07C9/20 | Using portable storage media (cards, keys) |
| G07C9/25 | Using biometric data |
| **H04L9** | Cryptographic mechanisms for digital credentials |

### Using CPC Codes

CPC codes provide the most precise searches because they classify patents by technology, not keywords:

```python
# All electronic lock patents
search_by_cpc("E05B47")

# Electronic locks granted in 2024+
search_by_cpc("E05B47", min_grant_date="20240101")

# Competitor's electronic locks
search_by_cpc("E05B47", assignee_filter="Allegion")

# Access control systems
search_by_cpc("G07C9")
```

**CPC Hierarchy:**
```
E             - Fixed Constructions
└── E05       - Locks; Keys; Window/Door Fittings
    └── E05B  - Locks; Accessories
        └── E05B47 - Electric/Magnetic operation
            └── E05B47/00 - Main group
            └── E05B47/02 - Circuits
            └── E05B47/06 - Remote control
```

**Look up CPC definitions:**
- Official: https://www.uspto.gov/web/patents/classification/cpc/html/cpc.html
- BigQuery: `SELECT * FROM patents-public-data.cpc.definition WHERE symbol LIKE 'E05B%'`

---

## Fallback Data Sources

When the USPTO ODP API is unavailable, the system falls back to alternative sources:

### 1. Google Patents API (Secondary)

**URL:** `https://patents.google.com/xhr/query`

- No API key required
- Rate limited (429 errors common)
- Less current than USPTO
- Good for historical searches

### 2. Google Patents BigQuery (Comprehensive)

**Dataset:** `patents-public-data.patents.publications`

- 150M+ patents worldwide
- Best CPC classification support
- Harmonized assignee names
- Requires Google Cloud account

See `docs/GOOGLE_PATENTS_BIGQUERY_ERD.md` for full schema documentation.

### 3. Sample Data (Demo)

When all APIs are unavailable, the system returns sample data for common queries to support demonstrations.

---

## Rate Limits & Error Handling

### USPTO ODP Limits

| Limit Type | Value |
|------------|-------|
| Requests per minute | 60 |
| Results per request | 100 max |
| Timeout | 30 seconds |

### Common Errors

| HTTP Code | Cause | Solution |
|-----------|-------|----------|
| 401 | Invalid API key | Check `USPTO_API_KEY` |
| 403 | Key revoked/expired | Get new key at data.uspto.gov |
| 429 | Rate limit exceeded | Wait 1 minute, retry |
| 500 | Server error | Retry with exponential backoff |
| 503 | Service unavailable | Use fallback (BigQuery) |

### Error Handling in Code

The `tools.patent_search` module handles errors automatically:

1. **401/403**: Prints authentication error, returns empty list
2. **429/5xx**: Falls back to Google Patents, then BigQuery
3. **Timeout**: Returns empty list after 30 seconds
4. **No API key**: Falls back to Google Patents immediately

---

## Official Documentation

- **USPTO Developer Portal:** https://developer.uspto.gov/
- **API Key Management:** https://data.uspto.gov/key/myapikey
- **Open Data Portal:** https://developer.uspto.gov/api-catalog
- **CPC Classification:** https://www.uspto.gov/web/patents/classification/cpc/html/cpc.html
- **Patent Data Bulk Download:** https://bulkdata.uspto.gov/

---

## Quick Reference

### Python Functions

```python
from tools import search_by_assignee, search_by_title, search_by_cpc

# Company search (works well as-is)
results = search_by_assignee("Allegion", limit=20)

# Keyword search - ALWAYS quote phrases!
results = search_by_title('"smart lock"', limit=20)
results = search_by_title('electronic AND deadbolt', limit=20)

# CPC search (most precise)
results = search_by_cpc("E05B47", min_grant_date="20240101")
results = search_by_cpc("E05B47", assignee_filter="Allegion")
```

### Verify Setup

```bash
# 1. Check API key configured
python3 -c "from tools.patent_search import _get_api_key; print('OK' if _get_api_key() else 'MISSING')"

# 2. Test search
python3 -c "from tools import search_by_assignee; print(search_by_assignee('Allegion', 3))"
```
