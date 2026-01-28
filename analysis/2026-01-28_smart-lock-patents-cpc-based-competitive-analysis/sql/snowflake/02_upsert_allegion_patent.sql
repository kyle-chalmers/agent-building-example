-- Snowflake: Upsert Allegion patent to cache
-- Executed: 2026-01-28
-- Result: 1 row inserted

MERGE INTO SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE.PATENTS AS target
USING (SELECT
    'US20260024390A1' AS patent_number,
    'ACCESS CONTROL ARCHITECTURE FOR DETECTING SECURE DATA COPIED BETWEEN DEVICES' AS title,
    '' AS abstract,
    'Schlage Lock Company LLC' AS assignee,
    PARSE_JSON('["Aaron Schlicht", "Joseph W. Baumgarte"]') AS inventors,
    '2025-09-30' AS filing_date,
    NULL AS grant_date,
    PARSE_JSON('["G07C   9/00309", "G07C2009/00388"]') AS cpc_codes,
    'Allegion' AS search_query,
    'competitor' AS category
) AS source
ON target.patent_number = source.patent_number
WHEN MATCHED THEN UPDATE SET
    title = source.title, abstract = source.abstract, assignee = source.assignee,
    inventors = source.inventors, filing_date = source.filing_date,
    grant_date = source.grant_date, cpc_codes = source.cpc_codes,
    search_query = source.search_query, category = source.category,
    updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN INSERT (
    patent_number, title, abstract, assignee, inventors, filing_date, grant_date,
    cpc_codes, search_query, category, created_at, updated_at
) VALUES (
    source.patent_number, source.title, source.abstract, source.assignee,
    source.inventors, source.filing_date, source.grant_date, source.cpc_codes,
    source.search_query, source.category, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()
);
