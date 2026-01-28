---
description: Generate a markdown competitor patent analysis report with full audit trail
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__snowflake__run_snowflake_query
---

# Competitor Report Generator

Company: $ARGUMENTS

## Instructions

1. **Create analysis workflow session:**
```bash
cd /Users/kylechalmers/Development/agent-building-example
python3 -c "
from tools import AnalysisWorkflow
workflow = AnalysisWorkflow('Competitor analysis: $ARGUMENTS')
print(f'Session: {workflow.folder_path}')
"
```

2. **Query Snowflake cache first:**
```sql
SELECT * FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS
WHERE assignee ILIKE '%{company}%'
ORDER BY filing_date DESC;
```

3. **If insufficient data, use USPTO API:**
```bash
cd /Users/kylechalmers/Development/agent-building-example
python3 -c "
from tools import search_by_assignee
import json
results = search_by_assignee('$ARGUMENTS', limit=50)
print(json.dumps(results, indent=2, default=str))
"
```

4. **If USPTO unavailable, query BigQuery (fallback - 150M+ patents):**
```bash
bq query --use_legacy_sql=false '
SELECT publication_number, title_localized[SAFE_OFFSET(0)].text as title,
       assignee_harmonized[SAFE_OFFSET(0)].name as assignee,
       filing_date, grant_date
FROM `patents-public-data.patents.publications`
WHERE EXISTS (
  SELECT 1 FROM UNNEST(assignee_harmonized) a
  WHERE LOWER(a.name) LIKE "%$ARGUMENTS%"
)
AND country_code = "US"
ORDER BY filing_date DESC
LIMIT 100'
```

5. **Analyze the data:**
   - Count patents by year
   - Identify technology categories (CPC codes E05B, E05C, G07C)
   - Find key inventors
   - Note recent filing activity

6. **Generate markdown report** using workflow:
```bash
cd /Users/kylechalmers/Development/agent-building-example
python3 -c "
from tools import generate_report_markdown
report = generate_report_markdown('$ARGUMENTS Competitor Analysis', patents, analysis_text)
print(report)
"
```

7. **Save to analysis folder** with all logged steps

8. **Confirm report location** to user
