# Patent Intelligence Agent Demo

## Overview
Build an intelligent agent that searches USPTO patent data for door hardware, locks, and access control innovations. The agent uses Snowflake as its primary data source, falling back to USPTO API only when needed. Reports are generated locally as markdown files.

**Key Design Principles:**
- Snowflake-first: Check database before making API calls
- Local reports: Markdown files in `./reports/` directory
- Best practices: Slim CLAUDE.md, modular skills, proper subagents
- No external API keys required

---

## Phase 1: Clean Repository
Delete all existing files:
- `thingiverse_client.py`, `test_api.py`, `test_api_simple.py`
- `example_usage.py`, `requirements.txt`
- `GETTING_CREDENTIALS.md`, `README.md`

Keep: `.gitignore`

---

## Phase 2: Create S3 Bucket (Optional Backup)
```bash
aws s3 mb s3://cad-designs-demo --region us-east-1
```

---

## Phase 3: Create Snowflake Schema & Table
Database: `SNOWFLAKE_LEARNING_DB`
Schema: Create `PATENT_INTELLIGENCE`

**Table: `PATENTS`**
- patent_number VARCHAR PRIMARY KEY
- title VARCHAR
- abstract TEXT
- assignee VARCHAR
- inventors VARIANT
- filing_date DATE
- grant_date DATE
- cpc_codes VARIANT
- search_query VARCHAR
- category VARCHAR
- created_at TIMESTAMP
- updated_at TIMESTAMP

---

## Phase 4: Build Patent Client Wrapper
**File: `patent_client_wrapper.py`**
- search_by_assignee(company, limit)
- search_by_title(keywords, limit)
- get_patent(patent_number)
- format_patent_for_storage(app)

---

## Phase 5: Build Patent Agent Module
**File: `patent_agent.py`**

**Snowflake-First Pattern:**
1. Check Snowflake for cached results
2. If cache miss or stale, call USPTO API
3. Store new results in Snowflake
4. Return combined results

**Core Functions:**
- search_competitor_patents(company)
- search_technology_patents(keywords)
- build_snowflake_query(search_type, query)
- build_upsert_query(patent_data)
- generate_report_markdown(title, patents)

---

## Phase 6: Local Markdown Reports
**Directory: `./reports/`**

Reports generated locally as markdown files.

---

## Phase 7: Project Structure

```
/agent-building-example
├── CLAUDE.md                     # Slim, actionable instructions
├── .gitignore
├── requirements.txt
├── patent_client_wrapper.py      # Thin API wrapper
├── patent_agent.py               # Core agent logic
├── demo.py                       # Interactive demo
├── reports/                      # Generated markdown reports
│   └── .gitkeep
├── .planning/                    # Planning docs
│   ├── PLAN.md
│   ├── CONTEXT.md
│   └── RESEARCH.md
├── .claude/
│   ├── agents/
│   │   └── patent-researcher.md
│   └── commands/
│       ├── patent-search.md
│       ├── competitor-report.md
│       └── patent-trends.md
└── tests/
    └── test_patent_agent.py
```

---

## Verification Plan

### Test 1: Patent Library Works
```python
from patent_client import USApplication
apps = list(USApplication.objects.filter(first_named_applicant="Allegion").limit(5))
assert len(apps) > 0
```

### Test 2: Snowflake Connection
Use MCP tool to query SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS

### Test 3: Natural Language Queries
- "Find recent smart lock patents from Allegion"
- "/competitor-report Dormakaba"
- "/patent-trends smart locks"
