-- Snowflake: Check cache for existing smart/electronic lock patents
-- Executed: 2026-01-28
-- Purpose: Check what patents already exist in Snowflake cache before API calls

SELECT patent_number, title, assignee, filing_date, search_query, category
FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS
WHERE (LOWER(title) LIKE '%residential%' AND LOWER(title) LIKE '%lock%')
   OR LOWER(title) LIKE '%smart lock%'
   OR LOWER(title) LIKE '%electronic lock%'
ORDER BY filing_date DESC
LIMIT 100;

-- Results: 3 rows returned
-- Patents found in cache:
--   US20250371921A1 - BEACON CIRCUIT FOR USE WITH ELECTRONIC LOCKS (ASSA ABLOY)
--   US20260017994A1 - ELECTRONIC LOCK COMPRISING INTERFACE CIRCUITRY (ASSA ABLOY)
--   US20260002382A1 - ENGAGEMENT MECHANISM FOR DISK DRIVE (Dormakaba)
