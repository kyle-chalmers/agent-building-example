# Example Analysis Prompt

Use this prompt to test the full patent analysis workflow.

---

## Prompt

```
Analyze smart lock patents filed in the last 2 years. I want to understand:
1. Which competitors are most active in this space
2. What specific technologies they're focusing on
3. Any emerging trends

Create a full analysis with audit trail.
```

---

## Expected Workflow

When you run this analysis, the agent should:

### 1. Create Analysis Session
```python
from tools import AnalysisWorkflow
workflow = AnalysisWorkflow("Smart lock patent analysis 2024-2026")
# Creates: analysis/2026-01-28_smart-lock-patent-analysis-2024-2026/
```

### 2. Check Snowflake Cache
```sql
SELECT * FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS
WHERE (title ILIKE '%smart lock%' OR abstract ILIKE '%smart lock%')
AND filing_date >= '2024-01-28'
ORDER BY filing_date DESC;
```

### 3. If Cache Miss, Use USPTO API
```python
from tools import search_by_title
results = search_by_title("smart lock", limit=50)
```

### 4. If USPTO Unavailable, Fall Back to BigQuery
```bash
bq query --use_legacy_sql=false '
SELECT
  publication_number,
  title_localized[SAFE_OFFSET(0)].text as title,
  assignee_harmonized[SAFE_OFFSET(0)].name as assignee,
  filing_date
FROM `patents-public-data.patents.publications`
WHERE EXISTS (
  SELECT 1 FROM UNNEST(cpc) c WHERE c.code LIKE "E05B47%"
)
AND country_code = "US"
AND filing_date >= 20240101
ORDER BY filing_date DESC
LIMIT 100'
```

### 5. Log All Steps
- Query results logged to `01_snowflake_queries.md`
- API/BigQuery calls logged to `02_api_results.md`
- Analysis steps logged to `03_analysis.md`

### 6. Generate Report
Final report in `04_report.md` with:
- Executive summary
- Competitor breakdown
- Technology trends
- Recommendations

---

## Output Structure

```
analysis/
└── 2026-01-28_smart-lock-patent-analysis-2024-2026/
    ├── metadata.json
    │   {
    │     "request": "Smart lock patent analysis 2024-2026",
    │     "started_at": "2026-01-28T...",
    │     "completed_at": "2026-01-28T...",
    │     "status": "complete"
    │   }
    ├── 01_snowflake_queries.md
    ├── 02_api_results.md
    ├── 03_analysis.md
    └── 04_report.md
```

---

## Verification Checklist

After running the analysis, verify:

- [ ] Analysis folder created in `analysis/`
- [ ] All 5 files present (metadata.json + 4 markdown files)
- [ ] metadata.json shows `"status": "complete"`
- [ ] Snowflake queries logged with results
- [ ] BigQuery/API calls logged with results
- [ ] Analysis steps documented
- [ ] Final report generated with insights
