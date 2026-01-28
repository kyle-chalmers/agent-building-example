-- BigQuery: Search access control systems by CPC code G07C9
-- Executed: 2026-01-28
-- Dataset: patents-public-data.patents.publications
-- Results: 100 patents returned

SELECT
    publication_number,
    title_localized[SAFE_OFFSET(0)].text as title,
    abstract_localized[SAFE_OFFSET(0)].text as abstract,
    assignee_harmonized[SAFE_OFFSET(0)].name as assignee,
    ARRAY_TO_STRING(ARRAY(SELECT name FROM UNNEST(inventor_harmonized)), ", ") as inventors,
    CAST(FLOOR(filing_date / 10000) AS STRING) || "-" ||
        LPAD(CAST(MOD(CAST(FLOOR(filing_date / 100) AS INT64), 100) AS STRING), 2, "0") || "-" ||
        LPAD(CAST(MOD(filing_date, 100) AS STRING), 2, "0") as filing_date,
    CAST(FLOOR(grant_date / 10000) AS STRING) || "-" ||
        LPAD(CAST(MOD(CAST(FLOOR(grant_date / 100) AS INT64), 100) AS STRING), 2, "0") || "-" ||
        LPAD(CAST(MOD(grant_date, 100) AS STRING), 2, "0") as grant_date,
    ARRAY_TO_STRING(ARRAY(SELECT code FROM UNNEST(cpc) WHERE code LIKE "G07C9%"), ", ") as cpc_codes
FROM `patents-public-data.patents.publications`
WHERE country_code = "US"
AND grant_date >= 20240101
AND EXISTS (SELECT 1 FROM UNNEST(cpc) c WHERE c.code LIKE "G07C9%")
ORDER BY grant_date DESC
LIMIT 100;
