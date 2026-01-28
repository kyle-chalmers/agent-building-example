-- BigQuery: Count patents by assignee for CPC E05B47 (electronic locks)
-- Executed: 2026-01-28
-- Dataset: patents-public-data.patents.publications
-- Purpose: Verify competitive landscape using CPC-based search

SELECT
    COUNT(*) as patent_count,
    assignee_harmonized[SAFE_OFFSET(0)].name as assignee
FROM `patents-public-data.patents.publications`
WHERE
    country_code = "US"
    AND grant_date >= 20240101
    AND EXISTS (
        SELECT 1 FROM UNNEST(cpc) c
        WHERE c.code LIKE "E05B47%"
    )
GROUP BY assignee
ORDER BY patent_count DESC
LIMIT 15;

-- Results:
-- | patent_count | assignee                        |
-- |--------------|---------------------------------|
-- | 29           | SCHLAGE LOCK CO LLC             |
-- | 15           | ASSA ABLOY AB                   |
-- | 14           | ASSA ABLOY AMERICAS RESIDENTIAL |
-- | 13           | HANCHETT ENTRY SYSTEMS INC      |
-- | 9            | DORMAKABA USA INC               |
-- | 7            | CAREFUSION 303 INC              |
-- | 7            | CARRIER CORP                    |
-- | 6            | TRITEQ LOCK AND SECURITY LLC    |
-- | 6            | INVUE SECURITY PRODUCTS INC     |
