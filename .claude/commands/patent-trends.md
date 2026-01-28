---
description: Analyze patent filing trends across competitors using Snowflake and BigQuery
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__snowflake__run_snowflake_query
---

# Patent Trends Analysis

Technology filter (optional): $ARGUMENTS

## Instructions

1. **Create analysis workflow session:**
```bash
cd /Users/kylechalmers/Development/agent-building-example
python3 -c "
from tools import AnalysisWorkflow
workflow = AnalysisWorkflow('Patent trends analysis: $ARGUMENTS')
print(f'Session: {workflow.folder_path}')
"
```

2. **Query Snowflake cache for trends:**
```sql
SELECT
    assignee,
    YEAR(filing_date) as year,
    COUNT(*) as patent_count
FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS
WHERE filing_date >= DATEADD(year, -5, CURRENT_DATE())
GROUP BY assignee, YEAR(filing_date)
ORDER BY year DESC, patent_count DESC;
```

3. **If technology filter provided, add to WHERE clause:**
```sql
AND (title ILIKE '%{technology}%' OR abstract ILIKE '%{technology}%')
```

4. **If Snowflake has insufficient data, use USPTO API:**
```bash
cd /Users/kylechalmers/Development/agent-building-example
python3 -c "
from tools import search_by_title
import json
results = search_by_title('$ARGUMENTS', limit=50)
print(json.dumps(results, indent=2, default=str))
"
```

5. **If USPTO unavailable, query BigQuery (fallback):**
```bash
bq query --use_legacy_sql=false '
SELECT
  assignee_harmonized[SAFE_OFFSET(0)].name as assignee,
  EXTRACT(YEAR FROM PARSE_DATE("%Y%m%d", CAST(filing_date AS STRING))) as year,
  COUNT(*) as patent_count
FROM `patents-public-data.patents.publications`
WHERE country_code = "US"
  AND filing_date >= 20190101
  AND EXISTS (
    SELECT 1 FROM UNNEST(cpc) c WHERE c.code LIKE "E05B%"
  )
GROUP BY assignee, year
ORDER BY year DESC, patent_count DESC
LIMIT 100'
```

6. **Analyze trends:**
   - Which company is most active?
   - Filing acceleration or deceleration?
   - Emerging technology areas?

7. **Generate markdown report** at `./analysis/{session}/04_report.md`

8. **Return summary** to user with session path
