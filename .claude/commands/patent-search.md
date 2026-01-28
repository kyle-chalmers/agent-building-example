---
description: Search patents. Checks Snowflake cache first, then BigQuery or USPTO API if needed.
allowed-tools:
  - Read
  - Bash
  - mcp__snowflake__run_snowflake_query
---

# Patent Search

User query: $ARGUMENTS

## Instructions

1. **Parse the query** to identify:
   - Company name (if searching by assignee)
   - Keywords (if searching by technology)
   - Date range (if specified)

2. **Check Snowflake cache first:**
```sql
SELECT * FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS
WHERE assignee ILIKE '%{company}%'
   OR title ILIKE '%{keywords}%'
ORDER BY filing_date DESC
LIMIT 20;
```

3. **If results found in Snowflake:**
   - Return formatted results
   - Note that these are cached results

4. **If cache miss, use USPTO API:**
```bash
cd /Users/kylechalmers/Development/agent-building-example
python3 -c "
from tools import search_by_assignee
results = search_by_assignee('{company}', limit=20)
for p in results:
    print(f\"[{p['patent_number']}] {p['title']}\")
    print(f\"  Assignee: {p['assignee']}\")
    print(f\"  Filed: {p['filing_date']}\")
    print()
"
```

5. **If USPTO unavailable, try BigQuery (fallback):**
```bash
bq query --use_legacy_sql=false '
SELECT publication_number, title_localized[SAFE_OFFSET(0)].text as title,
       assignee_harmonized[SAFE_OFFSET(0)].name as assignee,
       filing_date
FROM `patents-public-data.patents.publications`
WHERE EXISTS (
  SELECT 1 FROM UNNEST(assignee_harmonized) a
  WHERE LOWER(a.name) LIKE "%{company}%"
)
AND country_code = "US"
ORDER BY filing_date DESC
LIMIT 20'
```

6. **Store new results in Snowflake** using MCP tool

7. **Return formatted output** with:
   - Patent number, title, filing date
   - Assignee company
   - Brief abstract (first 200 chars)
   - Data source indicator (Snowflake/BigQuery/USPTO)
