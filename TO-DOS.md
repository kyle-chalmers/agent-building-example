# TO-DOS

## Completed

### ✅ Integrate USPTO Open Data Portal API - 2026-01-27

**Status:** COMPLETE

**Solution found:**
- Correct API endpoint: `https://api.uspto.gov/api/v1/patent/applications/search`
- Auth header: `X-API-KEY: <key>`
- Query param: `?q=<search_term>&rows=<limit>`

**Changes made:**
1. Updated `patent_client_wrapper.py` - USPTO ODP as primary, Google Patents as fallback
2. Updated `.env.example` - API key documentation
3. Updated `CLAUDE.md` - Available tools section for agents

**Results:**
- Allegion: 41 patents
- Dormakaba: 413 patents
- Total database: 12.6M+ patent applications

---

## Pending

### 🔍 Tool Limitations & Improvements Identified - 2026-01-28

**Context:** During smart lock patent analysis, several tool limitations were identified that could be improved for more comprehensive analysis.

#### 1. USPTO API Result Capping
**Issue:** The USPTO API appears to cap results at ~25-100 per query, even when requesting more (e.g., `limit=200`).
- Example: `search_by_assignee("Stanley Black & Decker", limit=100)` returns only 25 results despite API reporting 119,502 total matches.
- Impact: May miss relevant patents when analyzing large assignees.

**Potential Solutions:**
- Implement pagination using `start` parameter
- Add warning when results are capped
- Consider multiple search strategies (assignee variations, subsidiaries)

**Files affected:** `tools/patent_search.py` - `_search_uspto_odp()` function

---

#### 2. BigQuery CPC Search Date Filtering
**Issue:** `search_by_cpc()` uses `min_grant_date` parameter, but many patents are still applications (not yet granted).
- Impact: Misses recent patent applications that haven't been granted yet
- Example: Search for patents filed in 2024-2025 may miss applications still pending grant

**Potential Solutions:**
- Add `min_filing_date` parameter option
- Filter by both grant_date and filing_date in BigQuery query
- Document that grant_date filtering may miss recent applications

**Files affected:** `tools/patent_search.py` - `search_by_cpc()` function

---

#### 3. Missing Assignee Information
**Issue:** Some patents returned from USPTO API have empty assignee fields.
- Example: Several patents in results show `"assignee": ""`
- Impact: Competitor analysis may miss patents if assignee data is incomplete

**Potential Solutions:**
- Add fallback lookup for assignee information
- Use BigQuery harmonized assignee data when USPTO assignee is missing
- Document data quality limitations

**Files affected:** `tools/patent_search.py` - `_format_uspto_patent()` function

---

#### 4. Date Format Consistency
**Issue:** Date formats vary between USPTO API (YYYY-MM-DD) and BigQuery (YYYYMMDD).
- Current: Conversion handled in `search_by_cpc()` but could be more robust
- Impact: Date filtering may fail if formats don't match

**Potential Solutions:**
- Standardize date handling utility function
- Add date format validation
- Ensure consistent date comparison logic

**Files affected:** `tools/patent_search.py`, `run_smart_lock_analysis.py`

---

#### 5. Enhanced Competitor Search Strategy
**Suggestion:** Add support for searching subsidiaries and alternative company names.
- Example: "ASSA ABLOY" may file under "ASSA ABLOY AB", "ASSA ABLOY Americas", etc.
- Impact: More comprehensive competitor analysis

**Potential Solutions:**
- Add competitor alias mapping in `tools/__init__.py`
- Implement multi-name search for each competitor
- Aggregate results across all aliases

**Files affected:** `tools/__init__.py`, `tools/patent_search.py`

---

#### 6. Analysis Workflow Enhancement
**Suggestion:** Add support for incremental analysis updates.
- Current: Each analysis creates a new folder
- Potential: Allow updating existing analysis with new data

**Files affected:** `tools/analysis_workflow.py`

---

**Priority:** Medium - Tools work but could provide more comprehensive results with these improvements.
