-- BigQuery: Verify assignee data availability for recent patents
-- Executed: 2026-01-28
-- Dataset: patents-public-data.patents.publications
-- Purpose: Check why some patents have NULL assignees

SELECT
    publication_number,
    title_localized[SAFE_OFFSET(0)].text as title,
    assignee_harmonized[SAFE_OFFSET(0)].name as assignee,
    grant_date
FROM `patents-public-data.patents.publications`
WHERE country_code = "US"
AND grant_date >= 20240101
AND EXISTS (SELECT 1 FROM UNNEST(cpc) c WHERE c.code LIKE "E05B47%")
ORDER BY grant_date DESC
LIMIT 10;

-- Results showed most recent patents (Oct 21, 2025) have NULL assignees
-- because BigQuery data hasn't been fully updated yet.
-- Earlier patents (Oct 7-14) have complete assignee data.
