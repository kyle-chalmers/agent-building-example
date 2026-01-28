# Google Patents BigQuery - Entity Relationship Diagram

## Overview

The `patents-public-data` BigQuery project contains 20+ datasets with patent data from multiple sources. This ERD covers the most useful datasets for patent intelligence work.

---

## Dataset Summary

| Dataset | Description | Key Tables |
|---------|-------------|------------|
| `patents` | Google Patents core data (~150M publications) | publications |
| `google_patents_research` | ML annotations, embeddings | annotations, vector_db |
| `patentsview` | USPTO PatentsView mirror (normalized) | patent, assignee, inventor |
| `cpc` | CPC classification definitions | definition |
| `uspto_oce_pair` | USPTO PAIR prosecution data | application_data, transactions |
| `uspto_oce_assignment` | Patent ownership transfers | assignment, assignor, assignee |

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           GOOGLE PATENTS CORE                                    │
│                         (patents.publications)                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  patents.publications                                                            │
│  ═══════════════════                                                            │
│  PK: publication_number (STRING) ─── e.g., "US-7650331-B1"                      │
│  FK: family_id ──────────────────── Links related patents across countries      │
│  FK: application_number ─────────── Links to USPTO PAIR data                    │
│                                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐              │
│  │ Identifiers      │  │ Dates            │  │ Text Content     │              │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤              │
│  │ country_code     │  │ publication_date │  │ title_localized  │              │
│  │ kind_code        │  │ filing_date      │  │ abstract_localized│             │
│  │ application_kind │  │ grant_date       │  │ claims_localized │              │
│  │ pct_number       │  │ priority_date    │  │ description_*    │              │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘              │
│                                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐              │
│  │ Parties (ARRAY)  │  │ Classifications  │  │ References       │              │
│  ├──────────────────┤  │ (ARRAY)          │  │ (ARRAY)          │              │
│  │ inventor[]       │  ├──────────────────┤  ├──────────────────┤              │
│  │ inventor_harmon[]│  │ cpc[]            │  │ citation[]       │              │
│  │ assignee[]       │  │ ipc[]            │  │ priority_claim[] │              │
│  │ assignee_harmon[]│  │ uspc[]           │  │ parent[]         │              │
│  │ examiner[]       │  │ fi[], fterm[]    │  │ child[]          │              │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────────┘
         │
         │ publication_number
         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        RESEARCH ANNOTATIONS                                      │
│                   (google_patents_research.annotations)                          │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  google_patents_research.annotations                                             │
│  ═══════════════════════════════════                                            │
│  FK: publication_number ─────────── Links to patents.publications               │
│                                                                                  │
│  │ publication_number │ Clusters on publication_number + domain                 │
│  │ ocid               │ Open Concepts identifier                                │
│  │ preferred_name     │ Recognized entity name                                  │
│  │ domain             │ "chemistry", "biology", "technical"                     │
│  │ source             │ Annotation source                                       │
│  │ confidence         │ ML confidence score (0-1)                               │
│  │ character_offset_* │ Position in source text                                 │
│  │ inchi, smiles      │ Chemical identifiers (if chemistry domain)             │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  google_patents_research.vector_db                                               │
│  ═════════════════════════════════                                              │
│  Embeddings for semantic patent search                                           │
└─────────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────┐
│                         CPC CLASSIFICATION                                       │
│                           (cpc.definition)                                       │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│  cpc.definition                                                                  │
│  ═════════════                                                                  │
│  PK: symbol (STRING) ────────────── e.g., "E05B47/00"                           │
│  FK: parents, children ──────────── Hierarchical tree structure                 │
│                                                                                  │
│  │ symbol           │ CPC code (joins to patents.publications.cpc[].code)       │
│  │ titleFull        │ Full classification title                                 │
│  │ titlePart        │ Short title                                               │
│  │ definition       │ Detailed scope description                                │
│  │ level            │ Hierarchy depth (section→class→subclass→group)           │
│  │ parents          │ Parent CPC codes                                          │
│  │ children         │ Child CPC codes                                           │
│  │ ipcConcordant    │ Equivalent IPC code                                       │
└─────────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────┐
│                         USPTO PATENTSVIEW                                        │
│                    (Normalized relational schema)                                │
└─────────────────────────────────────────────────────────────────────────────────┘

                              ┌───────────────────┐
                              │     location      │
                              ├───────────────────┤
                              │ PK: id            │
                              │    city           │
                              │    state          │
                              │    country        │
                              │    latitude       │
                              │    longitude      │
                              └─────────┬─────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              │                         │                         │
              ▼                         ▼                         ▼
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│  location_inventor   │  │  location_assignee   │  │  patent_inventor     │
├──────────────────────┤  ├──────────────────────┤  ├──────────────────────┤
│ FK: location_id      │  │ FK: location_id      │  │ FK: patent_id        │
│ FK: inventor_id      │  │ FK: assignee_id      │  │ FK: inventor_id      │
└──────────┬───────────┘  └──────────┬───────────┘  │ FK: location_id      │
           │                         │              └──────────┬───────────┘
           │                         │                         │
           ▼                         ▼                         │
┌──────────────────────┐  ┌──────────────────────┐             │
│      inventor        │  │      assignee        │             │
├──────────────────────┤  ├──────────────────────┤             │
│ PK: id               │  │ PK: id               │             │
│    name_first        │  │    type              │             │
│    name_last         │  │    name_first        │             │
│    male_flag         │  │    name_last         │             │
│    attribution_status│  │    organization      │◄────────────┤
└──────────────────────┘  └──────────────────────┘             │
                                    ▲                          │
                                    │                          │
                          ┌────────┴────────┐                  │
                          │ patent_assignee │                  │
                          ├─────────────────┤                  │
                          │ FK: patent_id   │──────┐           │
                          │ FK: assignee_id │      │           │
                          │ FK: location_id │      │           │
                          └─────────────────┘      │           │
                                                   │           │
                                                   ▼           │
                                    ┌──────────────────────────┴──┐
                                    │           patent             │
                                    ├─────────────────────────────┤
                                    │ PK: id (patent_id)          │
                                    │    number                   │
                                    │    type                     │
                                    │    country                  │
                                    │    date                     │
                                    │    title                    │
                                    │    abstract                 │
                                    │    kind                     │
                                    │    num_claims               │
                                    └──────────────┬──────────────┘
                                                   │
                    ┌──────────────────────────────┼──────────────────────────────┐
                    │                              │                              │
                    ▼                              ▼                              ▼
         ┌──────────────────┐          ┌──────────────────┐          ┌──────────────────┐
         │  uspatentcitation│          │      claim       │          │    cpc_current   │
         ├──────────────────┤          ├──────────────────┤          ├──────────────────┤
         │ FK: patent_id    │          │ FK: patent_id    │          │ FK: patent_id    │
         │ FK: citation_id  │          │    text          │          │    section_id    │
         │    date          │          │    dependent     │          │    subsection_id │
         │    category      │          │    sequence      │          │    group_id      │
         │    sequence      │          └──────────────────┘          │    subgroup_id   │
         └──────────────────┘                                        │    sequence      │
                                                                     └──────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────┐
│                         USPTO PAIR (Prosecution History)                         │
│                            (uspto_oce_pair)                                      │
└─────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐          ┌──────────────────────────────┐
│        application_data              │          │        transactions          │
├──────────────────────────────────────┤          ├──────────────────────────────┤
│ PK: application_number               │◄────────►│ FK: application_number       │
│    filing_date                       │          │    event_code                │
│    invention_subject_matter          │          │    event_date                │
│    application_type                  │          │    event_description         │
│    examiner_name_*                   │          └──────────────────────────────┘
│    examiner_art_unit                 │
│    uspc_class/subclass               │          ┌──────────────────────────────┐
│    appl_status_code                  │          │       status_codes           │
│    appl_status_date                  │          ├──────────────────────────────┤
│    patent_number ────────────────────┼────►     │ PK: status_code              │
│    patent_issue_date                 │          │    status_description        │
│    abandon_date                      │          └──────────────────────────────┘
│    wipo_pub_number                   │
│    earliest_pgpub_number             │          ┌──────────────────────────────┐
└──────────────────────────────────────┘          │     continuity_parents       │
         │                                        ├──────────────────────────────┤
         │                                        │ FK: application_number       │
         ▼                                        │    parent_application_number │
┌──────────────────────────────────────┐          │    relationship_type         │
│          all_inventors               │          └──────────────────────────────┘
├──────────────────────────────────────┤
│ FK: application_number               │
│    inventor_name_*                   │
│    inventor_city/state/country       │
└──────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────────┐
│                      USPTO ASSIGNMENT (Ownership Changes)                        │
│                          (uspto_oce_assignment)                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐     ┌──────────────────────────┐
│       assignment         │     │       documentid         │
├──────────────────────────┤     ├──────────────────────────┤
│ PK: rf_id                │◄───►│ FK: rf_id                │
│    reel_no               │     │    doc_number (patent #) │
│    frame_no              │     │    type_cd               │
│    convey_text           │     └──────────────────────────┘
│    record_dt             │
└──────────────────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│assignor│ │assignee│  (Different from patentsview.assignee!)
├────────┤ ├────────┤
│ rf_id  │ │ rf_id  │
│ name   │ │ name   │
│ exec_dt│ │ address│
└────────┘ └────────┘
```

---

## Key Relationships for Patent Intelligence

### 1. Finding Patents by Company (Assignee)

```sql
-- Using patents.publications (denormalized, faster)
SELECT publication_number, title_localized[SAFE_OFFSET(0)].text
FROM `patents-public-data.patents.publications`
WHERE EXISTS (
  SELECT 1 FROM UNNEST(assignee_harmonized) a
  WHERE LOWER(a.name) LIKE '%allegion%'
)

-- Using patentsview (normalized, joins required)
SELECT p.number, p.title
FROM `patents-public-data.patentsview.patent` p
JOIN `patents-public-data.patentsview.patent_assignee` pa ON p.id = pa.patent_id
JOIN `patents-public-data.patentsview.assignee` a ON pa.assignee_id = a.id
WHERE LOWER(a.organization) LIKE '%allegion%'
```

### 2. CPC Classification Lookup

```sql
-- Get CPC definition for a code
SELECT symbol, titleFull, definition
FROM `patents-public-data.cpc.definition`
WHERE symbol = 'E05B47/00'  -- Locks operated by electric/magnetic means

-- Find patents in a CPC class
SELECT publication_number
FROM `patents-public-data.patents.publications`
WHERE EXISTS (
  SELECT 1 FROM UNNEST(cpc) c WHERE c.code LIKE 'E05B47%'
)
```

### 3. Tracking Ownership Changes

```sql
-- Find assignment history for a patent
SELECT a.convey_text, a.record_dt,
       aor.name as from_entity,
       aee.name as to_entity
FROM `patents-public-data.uspto_oce_assignment.assignment` a
JOIN `patents-public-data.uspto_oce_assignment.documentid` d ON a.rf_id = d.rf_id
JOIN `patents-public-data.uspto_oce_assignment.assignor` aor ON a.rf_id = aor.rf_id
JOIN `patents-public-data.uspto_oce_assignment.assignee` aee ON a.rf_id = aee.rf_id
WHERE d.doc_number = '10123456'
```

---

## Table Sizes (Approximate)

| Table | Rows | Size |
|-------|------|------|
| patents.publications | ~150M | ~3 TB |
| google_patents_research.annotations | ~2B | ~500 GB |
| patentsview.patent | ~8M | ~10 GB |
| uspto_oce_pair.application_data | ~12M | ~50 GB |
| cpc.definition | ~260K | ~500 MB |

---

## Recommended Approach for Competitive Analysis

**Primary table: `patents.publications`** - Use this for most queries. It's denormalized (no joins needed) and optimized for searches by assignee, CPC codes, and dates. The `assignee_harmonized` field provides clean company names.

**Secondary table: `uspto_oce_assignment.*`** - Use this to track competitor acquisitions and IP transfers. When a competitor buys a company or acquires a patent portfolio, it shows up here before the main publications table is updated.

### Recommended Query Strategy

1. **Daily monitoring**: Query `patents.publications` filtered by competitor names + recent `publication_date`
2. **M&A intelligence**: Query `uspto_oce_assignment` for transfers involving competitor names
3. **Technology landscaping**: Query `patents.publications` by CPC codes (E05B* for locks/access control)
4. **Deep dives**: Use `patentsview` normalized tables when you need inventor networks or citation analysis

### Use Case → Table Mapping

| Use Case | Primary Table | Notes |
|----------|---------------|-------|
| Competitor patent counts | patents.publications | Use assignee_harmonized |
| Technology trends | patents.publications | Filter by CPC codes E05B* |
| Patent citations | patentsview.uspatentcitation | Normalized, easier to query |
| Prosecution history | uspto_oce_pair.application_data | Examiner info, status |
| Ownership transfers | uspto_oce_assignment.* | M&A activity detection |

---

## Access Information

- **Project**: `patents-public-data`
- **Authentication**: Requires Google Cloud account
- **Billing**: Free tier covers most queries; ~$5/TB scanned after
- **CLI**: `bq query --use_legacy_sql=false 'SELECT ...'`
