-- Snowflake: Verify patent cache counts by competitor
-- Executed: 2026-01-28
-- Purpose: Confirm patents were cached correctly

SELECT search_query, COUNT(*) as count
FROM SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS
GROUP BY search_query
ORDER BY count DESC;

-- Results:
-- | search_query          | count |
-- |-----------------------|-------|
-- | Dormakaba             | 18    |
-- | Stanley Black & Decker| 17    |
-- | ASSA ABLOY            | 17    |
-- | Allegion              | 15    |
-- | Spectrum Brands       | 13    |
