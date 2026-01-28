# USPTO/Google Patents API Calls

## API Call 1: Search Allegion patents with electronic lock classification (E05B47)

**Endpoint:** `BigQuery CPC Search`

**Parameters:**
```json
{
  "cpc_code": "E05B47",
  "assignee_filter": "Allegion",
  "limit": 50
}
```

**Results:** 0 items returned

---

## API Call 2: Search for smart lock patents using quoted phrase

**Endpoint:** `USPTO API Title Search`

**Parameters:**
```json
{
  "query": "\"smart lock\"",
  "limit": 200
}
```

**Results:** 25 items returned

<details>
<summary>Preview (first 5 results)</summary>

```json
[
  {
    "patent_number": "US20250362098A1",
    "title": "SMART LOCK",
    "abstract": "",
    "assignee": "",
    "inventors": [
      "Shawn Kitchell",
      "Patrick Farchione JR.",
      "Phillip Thomas Farchione"
    ],
    "filing_date": "2025-05-23",
    "grant_date": null,
    "cpc_codes": [
      "F41A  17/063"
    ],
    "status_code": 30
  },
  {
    "patent_number": "",
    "title": "Smart lock",
    "abstract": "",
    "assignee": "TCL Smart Home Technologies Co., Ltd.",
    "inventors": [
      "Kerong FU",
      "Xiaofeng XIAO",
      "Yan Zhu"
    ],
    "filing_date": "2025-05-21",
    "grant_date": null,
    "cpc_codes": [],
    "status_code": 30
  },
  {
    "patent_number": "US20250230685A1",
    "title": "ASSEMBLY, SYSTEM, AND METHOD FOR OPERATIVELY ASSOCIATING A SMART LOCK TO A BARRIER",
    "abstract": "",
    "assignee": "",
    "inventors": [
      "David Michael Skupien"
    ],
    "filing_date": "2025-01-13",
    "grant_date": null,
    "cpc_codes": [
      "E05B  47/0001",
      "E05B  65/46",
      "E05B2047/0091"
    ],
    "status_code": 30
  },
  {
    "patent_number": "",
    "title": "Smart Lock",
    "abstract": "",
    "assignee": "Shenzhen Qirui Industrial Co., LTD",
    "inventors": [
      "Shengbo WANG"
    ],
    "filing_date": "2024-12-11",
    "grant_date": null,
    "cpc_codes": [],
    "status_code": 150
  },
  {
    "patent_number": "",
    "title": "SMART LOCK SYSTEM",
    "abstract": "",
    "assignee": "ONES BILISIM TEKNOLOJILER ANONIM SIRKETI",
    "inventors": [
      "Dursun Dogukan GOZEN",
      "Engin CAN",
      "Gucluhan KUZYAKA",
      "Gurol Erkin GURBUZ",
      "Onur SIRMATEL"
    ],
    "filing_date": "2024-12-02",
    "grant_date": null,
    "cpc_codes": [],
    "status_code": 30
  }
]
```
</details>

---

