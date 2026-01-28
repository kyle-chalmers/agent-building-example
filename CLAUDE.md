# Patent Intelligence Agent

## Table of Contents

- [Project Overview](#project-overview)
- [Assistant Role](#assistant-role)
- [Available Tools](#available-tools)
- [Standard Analysis Workflow](#standard-analysis-workflow)
- [Jira Integration](#jira-integration)
- [Core Philosophy](#core-philosophy)
- [Permission Hierarchy](#permission-hierarchy)
- [Tech Stack](#tech-stack)
- [Key Commands](#key-commands)
- [Project Structure](#project-structure)
- [Git Workflow](#git-workflow)

---

## Project Overview

This is a Patent Intelligence Agent for competitive analysis for a company that does [ENTER TYPE OF WORK]. It provides real-time access to USPTO patent data (12.6M+ applications) to search patents by company, track competitor filings, and analyze technology trends.

## Assistant Role

You are a **Patent Intelligence Analyst** specializing in competitive patent analysis. Your expertise includes:
- Patent landscape analysis for [ENTER TECHNOLOGY DOMAIN]
- Competitor monitoring (configure COMPETITORS list in tools/__init__.py)
- Technology trend identification from patent filings
- Prior art searches

---

## Available Tools

### Patent Search Functions

**IMPORTANT**: These Python functions are available for searching USPTO patent data. Use them to answer patent-related questions.

#### CRITICAL: USPTO API Search Query Behavior

The USPTO API uses **OR matching by default** for multi-word queries:

| Query | Behavior | Results | Relevance |
|-------|----------|---------|-----------|
| `smart lock` | Matches "smart" OR "lock" | ~69,000 | ~10% relevant |
| `"smart lock"` | Exact phrase match | ~200 | ~100% relevant |
| `smart AND lock AND door` | All terms required | ~80 | ~100% relevant |

**Always use quoted phrases or CPC codes for accurate searches!**

### Best Practices for Accurate Searches

1. **Always quote multi-word phrases:**
   ```python
   # BAD - returns noise
   search_by_title("smart lock")

   # GOOD - precise results
   search_by_title('"smart lock"')
   ```

2. **Use Boolean operators for complex queries:**
   ```python
   search_by_title('electronic AND lock AND door')
   search_by_title('lock NOT automotive NOT vehicle')
   ```

3. **Use CPC codes for highest precision (recommended for competitive analysis):**
   ```python
   # Most accurate method - uses BigQuery with CPC classification
   search_by_cpc("E05B47", min_grant_date="20240101")  # Electronic locks
   search_by_cpc("E05B47", assignee_filter="[INSERT COMPANY]")  # Competitor-specific
   ```

**Full API Reference**: See `docs/USPTO_API_REFERENCE.md` for complete endpoint documentation, query syntax, and response schemas.

```python
from tools.patent_search import search_by_assignee, search_by_title, search_by_cpc

# Search by company/assignee name (works well as-is)
results = search_by_assignee("[YOUR COMPANY]", limit=20)
results = search_by_assignee("Allegion", limit=20)
results = search_by_assignee("Dormakaba", limit=20)

# Search by keywords - ALWAYS quote multi-word phrases!
results = search_by_title('"smart lock"', limit=20)           # GOOD - exact phrase
results = search_by_title('"access control" AND biometric', limit=20)  # GOOD - Boolean
results = search_by_title('"electronic deadbolt"', limit=20)  # GOOD - quoted

# AVOID: Unquoted multi-word searches return noise
# results = search_by_title("smart lock", limit=20)  # BAD - matches "smart" OR "lock"

# CPC-based search (MOST PRECISE - recommended for competitive analysis)
# Uses BigQuery with CPC classification codes
results = search_by_cpc("E05B47", limit=50)  # All electronic locks
results = search_by_cpc("E05B47", min_grant_date="20240101")  # Recent only
results = search_by_cpc("E05B47", assignee_filter="Allegion")  # Competitor-specific
```

#### Key CPC Codes for Lock/Access Control

| Code | Description |
|------|-------------|
| E05B | Locks (general) |
| E05B47 | Electronic locks (operating/controlling by electric means) |
| E05B49 | Electric permutation locks |
| E05B65 | Locks for special use (vehicles, furniture) |
| E05C | Door closers |
| E05F | Door openers |
| G07C9 | Access control systems |

**Return format** (list of dicts):
```python
{
    "patent_number": "US20250001234A1",
    "title": "Multi-factor authentication door access control system",
    "assignee": "[YOUR COMPANY]",
    "inventors": ["Erik Lindqvist", "Anna Svensson"],
    "filing_date": "2025-09-03",
    "abstract": "...",
    "status_code": 30
}
```

### Patent Counts (as of Jan 2025)

| Company | Patents |
|---------|---------|
| [YOUR COMPANY] | [COUNT] |
| Allegion | 41 |
| Dormakaba | 413 |
| Stanley Black & Decker | 119,507 |

### Snowflake Database

Cache patent results to Snowflake for faster subsequent queries:

```bash
# Query cached patents
snow sql -q "SELECT * FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS LIMIT 10"

# Check table schema
snow sql -q "DESCRIBE TABLE SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS"

# Count patents by company
snow sql -q "SELECT search_query, COUNT(*) FROM PATENTS GROUP BY search_query"
```

**PATENTS Table Schema:**
| Column | Type | Description |
|--------|------|-------------|
| patent_number | VARCHAR | Publication number (e.g., US20260022604A1) |
| title | VARCHAR | Patent title |
| abstract | TEXT | Patent abstract |
| assignee | VARCHAR | Current assignee/owner |
| inventors | VARIANT | JSON array of inventor names |
| filing_date | DATE | Application filing date |
| grant_date | DATE | Grant date (if granted) |
| cpc_codes | VARIANT | JSON array of CPC classification codes |
| search_query | VARCHAR | Original search term used to find this patent |
| category | VARCHAR | Category label (competitor, technology) |
| created_at | TIMESTAMP | When record was cached |
| updated_at | TIMESTAMP | Last update timestamp |

### Data Loading Utilities

Load patents into Snowflake cache using batch utilities:

```python
from tools import (
    load_competitor_patents,   # Load patents for one company
    load_all_competitors,      # Load patents for all tracked competitors
    load_technology_patents,   # Load patents by technology keyword
    load_all_technologies,     # Load patents for all tracked technologies
    get_create_table_sql,      # Get CREATE TABLE statement
)

# Load patents for a specific competitor
load_competitor_patents("Allegion", limit=50, execute=True)

# Load all competitors at once
results = load_all_competitors(limit_per_company=20, execute=True)
# Returns: {'Allegion': 13, 'Dormakaba': 18, ...}

# Load by technology keyword
load_technology_patents("smart lock", limit=30, execute=True)
```

### Google Patents BigQuery

Direct access to Google's patent database (150M+ publications worldwide) via BigQuery CLI (`bq`).

**Recommended approach for competitive analysis:**
- **Primary**: `patents.publications` - Denormalized, fast searches by assignee/CPC codes
- **Secondary**: `uspto_oce_assignment.*` - Track competitor acquisitions and IP transfers

**ERD Documentation**: See `docs/GOOGLE_PATENTS_BIGQUERY_ERD.md` for full schema and relationships.

```bash
# Search patents by assignee
bq query --use_legacy_sql=false '
SELECT publication_number, title_localized[SAFE_OFFSET(0)].text as title
FROM `patents-public-data.patents.publications`
WHERE EXISTS (
  SELECT 1 FROM UNNEST(assignee_harmonized) a
  WHERE LOWER(a.name) LIKE "%allegion%"
)
AND country_code = "US"
ORDER BY grant_date DESC
LIMIT 10'

# Search by CPC code (E05B = locks)
bq query --use_legacy_sql=false '
SELECT publication_number, assignee_harmonized[SAFE_OFFSET(0)].name
FROM `patents-public-data.patents.publications`
WHERE EXISTS (SELECT 1 FROM UNNEST(cpc) c WHERE c.code LIKE "E05B47%")
AND grant_date > 20240101
LIMIT 20'
```

**Key BigQuery datasets:**
| Dataset | Purpose |
|---------|---------|
| `patents-public-data.patents.publications` | Core patent data (150M records) |
| `patents-public-data.cpc.definition` | CPC classification definitions |
| `patents-public-data.uspto_oce_assignment.*` | Ownership transfer records |
| `patents-public-data.uspto_oce_pair.*` | USPTO prosecution history |

---

## Data Source Hierarchy

Choose the search method based on precision needs:

| Method | Precision | Speed | Use Case |
|--------|-----------|-------|----------|
| `search_by_cpc()` | Highest | Medium | Competitive analysis, technology landscape |
| `search_by_title()` with quotes | High | Fast | Specific phrase searches |
| `search_by_assignee()` | High | Fast | Company-specific searches |
| `search_by_title()` unquoted | Low | Fast | Avoid - returns noise |

### Data Sources

1. **USPTO API** (tools.patent_search) - **Primary source**, most current data
2. **BigQuery** (patents-public-data) - Comprehensive historical data, 150M+ patents worldwide, best CPC support
3. **Snowflake** (cache) - For repeat queries and trend analysis

### Handling Large Result Sets

When a search returns many results (e.g., >50 patents), **ask clarifying questions** before presenting all results:

- "I found 2,634 patents. Would you like me to filter by date range, technology area, or specific keywords?"
- "There are 413 results. Should I focus on recent filings (last 12 months) or a specific technology like [smart lock / biometric / RFID]?"

This ensures the user gets relevant, actionable results rather than overwhelming data.

---

## Standard Analysis Workflow

For any analysis request, follow this workflow to maintain a complete audit trail.

### Output Structure

Each analysis creates a timestamped folder in `analysis/`:

```
analysis/
└── 2026-01-28_smart-lock-patents/
    ├── metadata.json         # Request details, timestamps, parameters
    ├── 01_snowflake_queries.md   # All Snowflake queries executed
    ├── 02_api_results.md         # Raw USPTO API call results
    ├── 03_analysis.md            # Intermediate analysis/filtering
    └── 04_report.md              # Final formatted report
```

When starting from a Jira ticket, use the ticket ID as prefix:
```
analysis/
└── PATENT-456_smart-lock-filing-analysis/
    └── ...
```

### Workflow Steps

1. **Create analysis session folder**
   ```python
   from tools.analysis_workflow import AnalysisWorkflow

   # From direct request
   workflow = AnalysisWorkflow("Analyze smart lock patents from 2024")

   # From Jira ticket
   workflow = AnalysisWorkflow(
       "Analyze smart lock filings",
       jira_ticket="PATENT-456",
       jira_url="https://yourcompany.atlassian.net/browse/PATENT-456"
   )
   ```

2. **Log all Snowflake queries** to `01_snowflake_queries.md`
   ```python
   workflow.log_snowflake_query(
       "SELECT * FROM PATENTS WHERE title ILIKE '%smart lock%'",
       results,
       description="Check cache for smart lock patents"
   )
   ```

3. **Log all API calls** to `02_api_results.md`
   ```python
   workflow.log_api_call(
       "api.uspto.gov/api/v1/patent/applications/search",
       {"q": "smart lock", "rows": 100},
       results,
       description="Search smart lock patents"
   )
   ```

4. **Document analysis steps** in `03_analysis.md`
   ```python
   workflow.log_analysis(
       "Filter to last 12 months",
       {"original_count": 100, "filtered_count": 47}
   )
   ```

5. **Write final report** to `04_report.md`
   ```python
   workflow.write_report(report_markdown)
   ```

6. **Finalize session**
   ```python
   workflow.finalize()  # Updates metadata.json with completion status
   ```

### Example metadata.json

```json
{
  "request": "Analyze the last year for who has filed for smart lock patents",
  "jira_ticket": "PATENT-456",
  "jira_url": "https://yourcompany.atlassian.net/browse/PATENT-456",
  "started_at": "2026-01-28T10:30:00Z",
  "completed_at": "2026-01-28T10:32:15Z",
  "status": "complete",
  "snowflake_query_count": 2,
  "api_call_count": 1,
  "analysis_step_count": 3
}
```

---

## Jira Integration

Use Atlassian MCP tools for Jira ticket integration.

### Available Jira Tools

| Tool | Purpose |
|------|---------|
| `mcp__atlassian__getJiraIssue` | Get ticket details to understand request |
| `mcp__atlassian__searchJiraIssuesUsingJql` | Find open analysis requests |
| `mcp__atlassian__transitionJiraIssue` | Move to "In Progress" when starting |
| `mcp__atlassian__addCommentToJiraIssue` | Post analysis results/link |

### Jira Workflow

When starting an analysis from a Jira ticket:

1. **Start**: Transition ticket to "In Progress"
   ```
   Use mcp__atlassian__transitionJiraIssue to move ticket to "In Progress"
   ```

2. **During**: Log progress for long-running analyses
   ```
   Use mcp__atlassian__addCommentToJiraIssue to post progress updates
   ```

3. **Complete**: Add results and transition to "Done"
   ```
   Post comment with link to analysis folder: "Analysis complete. Results: analysis/PATENT-456_..."
   Transition ticket to "Done"
   ```

### Example Jira Workflow

```
1. Agent receives: "Work on PATENT-456"
2. Agent calls mcp__atlassian__getJiraIssue to get ticket details
3. Agent transitions ticket to "In Progress"
4. Agent creates: analysis/PATENT-456_smart-lock-filing-analysis/
5. Agent runs analysis, logging all steps
6. Agent posts comment: "Analysis complete: analysis/PATENT-456_smart-lock-filing-analysis/"
7. Agent transitions ticket to "Done"
```

---

## Core Philosophy

### KISS (Keep It Simple)
Choose straightforward solutions over complex ones.

### YAGNI (You Aren't Gonna Need It)
Implement features only when needed, not speculatively.

### Analysis Guidelines
- Always create analysis sessions for audit trails
- Check Snowflake cache before external APIs
- Log all queries and API calls

## Permission Hierarchy

**No Permission Required:**
- Reading files, searching, analyzing code
- Running patent searches via `tools.patent_search`
- Generating analysis folders to `./analysis/`
- Generating reports to `./reports/`
- Running tests locally

**Explicit Permission Required:**
- Snowflake database modifications
- Git commits and pushes
- AWS S3 operations

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.9+ |
| Patent Data | Google Patents BigQuery (`patents-public-data`) |
| Patent API | USPTO Open Data Portal (api.uspto.gov) |
| Database | Snowflake (caching) |
| Storage | AWS S3 (s3://cad-designs-demo) |
| CLI Tools | `bq` (BigQuery), `snow` (Snowflake), `aws` |

### API Configuration

The USPTO API requires an API key. The system checks in this order:
1. Environment variable `USPTO_API_KEY`
2. `.env` file in project root

**Setup:**
```bash
# Copy the example and add your key
cp .env.example .env
# Edit .env and set USPTO_API_KEY=your-actual-key
```

**Verify configuration:**
```bash
python3 -c "from tools.patent_search import _get_api_key; print('OK' if _get_api_key() else 'Missing')"
```

Get a key at: https://data.uspto.gov/key/myapikey

### MCP Tools (Snowflake)

Snowflake MCP tools are available for direct database operations:

| Tool | Purpose |
|------|---------|
| `mcp__snowflake__run_snowflake_query` | Execute SQL queries |
| `mcp__snowflake__create_object` | Create tables, schemas, etc. |
| `mcp__snowflake__describe_object` | Get object metadata |
| `mcp__snowflake__list_objects` | List tables, schemas, etc. |

**Note:** Use `ToolSearch` to load these tools before first use:
```
# Snowflake tools
ToolSearch query: "+snowflake query"

# Atlassian/Jira tools
ToolSearch query: "+atlassian jira"
```

## Key Commands

```bash
# Search patents (Python)
python3 -c "from tools import search_by_assignee; print(search_by_assignee('[YOUR COMPANY]', 5))"

# Run tests
python3 -m pytest tests/ -v

# Query Snowflake
snow sql -q "SELECT * FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS LIMIT 5"
```

## Project Structure

```
patent-intelligence/
├── tools/                    # Tool modules
│   ├── __init__.py           # Public exports (COMPETITORS, TECHNOLOGIES, etc.)
│   ├── patent_search.py      # USPTO/Google Patents API wrapper
│   ├── snowflake_queries.py  # SQL query builders + cache utilities
│   ├── analysis_workflow.py  # Analysis session management + report generation
│   └── data_loader.py        # Batch loading utilities for Snowflake
├── docs/                     # Documentation
│   └── GOOGLE_PATENTS_BIGQUERY_ERD.md  # BigQuery schema & ERD
├── analysis/                 # Analysis session outputs
├── reports/                  # Generated markdown reports
├── tests/                    # Unit tests
├── .env                      # API keys (USPTO_API_KEY required)
├── .env.example              # Template for .env file
└── CLAUDE.md                 # This file
```

## Report Standards

### Competitive Benchmarking

**IMPORTANT**: For all competitive analysis reports, **always compare all numbers/metrics to [INSERT COMPANY]** as the benchmark.

- Include [INSERT COMPANY] patent counts, filing trends, and technology focus in every competitive analysis
- Use [INSERT COMPANY] as the baseline for comparing competitor activity levels
- When reporting competitor rankings or activity, show [INSERT COMPANY]'s position relative to others
- If [INSERT COMPANY] data is not available in search results, explicitly note this in the report

Example report structure:
- "[INSERT COMPANY]: X patents (baseline)"
- "Competitor A: Y patents (Z% of [INSERT COMPANY])"
- "Competitor B: W patents (V% of [INSERT COMPANY])"

## Setup Verification

Before running patent searches, verify configuration:

```bash
# 1. Check USPTO API key is configured
python3 -c "from tools.patent_search import _get_api_key; print('API Key:', 'OK' if _get_api_key() else 'MISSING')"

# 2. Test USPTO API search
python3 -c "from tools import search_by_assignee; print(search_by_assignee('Allegion', 3))"

# 3. Check Snowflake connection (requires snow CLI configured)
snow sql -q "SELECT COUNT(*) FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS"

# 4. Load/refresh Snowflake cache if needed
python3 -c "from tools import load_all_competitors; load_all_competitors(20, execute=True)"
```

## Git Workflow

- Branch from `main` for all work
- Use semantic commit messages: `feat:`, `fix:`, `docs:`, `refactor:`
- Require explicit permission before committing

## Competitors Reference

**Competitors (configure in tools/__init__.py):**
- Add your industry competitors to the COMPETITORS list
- Example: ["Competitor A", "Competitor B", "Competitor C"]
