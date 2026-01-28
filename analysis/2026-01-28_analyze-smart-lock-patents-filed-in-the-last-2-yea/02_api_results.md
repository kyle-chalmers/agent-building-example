# USPTO/Google Patents API Calls

## API Call 1: Search Allegion patents, filtered to last 2 years

**Endpoint:** `api.uspto.gov/api/v1/patent/applications/search (assignee: Allegion)`

**Parameters:**
```json
{
  "q": "Allegion",
  "rows": 100
}
```

**Results:** 8 items returned

<details>
<summary>Preview (first 5 results)</summary>

```json
[
  {
    "patent_number": "US20260022604A1",
    "title": "DOOR SYSTEM HAVING A SWING INTERLOCK SYSTEM",
    "abstract": "",
    "assignee": "Allegion Access Technologies LLC",
    "inventors": [
      "Vinay N. Patel",
      "Thomas M. Kowalczyk",
      "Ronald Laliberte",
      "James Cavanaugh"
    ],
    "filing_date": "2025-05-06",
    "grant_date": null,
    "cpc_codes": [
      "E05D  15/58",
      "E05C  19/16",
      "E05Y2900/132",
      "E06B   3/509"
    ],
    "status_code": 30
  },
  {
    "patent_number": "US20250297514A1",
    "title": "CONNECTION SYSTEM FOR A HEADER AND A JAMB OF A DOOR ASSEMBLY",
    "abstract": "",
    "assignee": "Allegion Access Technologies LLC",
    "inventors": [
      "Benjamin Marotte",
      "James Cavanaugh",
      "Ronald R. Laliberte",
      "Vinay Patel"
    ],
    "filing_date": "2025-03-04",
    "grant_date": null,
    "cpc_codes": [
      "E06B   3/9624",
      "E06B   3/9642",
      "E06B   3/9687"
    ],
    "status_code": 30
  },
  {
    "patent_number": "US20250122759A1",
    "title": "AUTOMATIC DOOR WITH RADAR SENSING",
    "abstract": "",
    "assignee": "ALLEGION ACCESS TECHNOLOGIES LLC",
    "inventors": [
      "Jorge I Guevara Rosas",
      "Jonathan M. Braverman",
      "Anthony R. Ranaudo",
      "Pedro I. I\u00f1igo Santiago",
      "Ethan F. Traineanu",
      "Kyle N. Carissimi",
      "Christopher Conroy"
    ],
    "filing_date": "2024-12-23",
    "grant_date": null,
    "cpc_codes": [
      "E05F  15/73",
      "E05Y2400/40",
      "E05Y2400/44",
      "E05Y2400/45",
      "E05Y2900/132",
      "G01S   7/40",
      "G01S  13/726",
      "G01S  13/88",
      "E05Y2800/30",
      "G01S  13/86"
    ],
    "status_code": 30
  },
  {
    "patent_number": "US20250257587A1",
    "title": "SLIDE LATCHING SYSTEM FOR A DOOR SYSTEM",
    "abstract": "",
    "assignee": "Allegion Access Technologies LLC",
    "inventors": [
      "Vinay N. Patel",
      "Thomas M. Kowalczyk",
      "Ronald R. Laliberte",
      "James Cavanaugh",
      "Daniel R. Seymour"
    ],
    "filing_date": "2024-12-17",
    "grant_date": null,
    "cpc_codes": [
      "E05B   7/00",
      "E05B  65/0811",
      "E05B  15/0205",
      "E05B  65/08",
      "E05C   3/162",
      "E05C   3/167"
    ],
    "status_code": 30
  },
  {
    "patent_number": "",
    "title": "SLIDING DOOR SYSTEM AND ROLLER GUIDE FOR THE SAME",
    "abstract": "",
    "assignee": "ALLEGION ACCESS TECHNOLOGIES LLC",
    "inventors": [
      "AARON ROSE",
      "CHRISTOPHER E. KOLODZIEJ",
      "PAUL N. GORGAS",
      "VINAY PATEL",
      "TODD STRICKLER",
      "THUAN VAN NGUYEN",
      "GARY BARCH"
    ],
    "filing_date": "2024-08-19",
    "grant_date": null,
    "cpc_codes": [],
    "status_code": 566
  }
]
```
</details>

---

## API Call 2: Search Dormakaba patents, filtered to last 2 years

**Endpoint:** `api.uspto.gov/api/v1/patent/applications/search (assignee: Dormakaba)`

**Parameters:**
```json
{
  "q": "Dormakaba",
  "rows": 100
}
```

**Results:** 25 items returned

<details>
<summary>Preview (first 5 results)</summary>

```json
[
  {
    "patent_number": "US20250390369A1",
    "title": "METHOD FOR UNBOLTING AN ACCESS SYSTEM USING A MOBILE DEVICE AND/OR FOR ERROR DETECTION, RELATING TO AN UNBOLTING OF AN ACCESS SYSTEM; READING DEVICE; SYSTEM; COMPUTER PROGRAM PRODUCT",
    "abstract": "",
    "assignee": "DORMAKABA SCHWEIZ AG",
    "inventors": [
      "Christian RAPPEL"
    ],
    "filing_date": "2025-09-08",
    "grant_date": null,
    "cpc_codes": [
      "G06F  11/0757",
      "G06F   8/65",
      "G06F  11/0742",
      "G07C   9/00309"
    ],
    "status_code": 19
  },
  {
    "patent_number": "US20260009270A1",
    "title": "MONITORING DEVICE FOR A DOOR FUNCTIONAL UNIT",
    "abstract": "",
    "assignee": "dormakaba Deutschland GmbH",
    "inventors": [
      "Michael THIELE",
      "Alexander HELLWIG"
    ],
    "filing_date": "2025-06-30",
    "grant_date": null,
    "cpc_codes": [
      "E05F   1/10",
      "E05Y2201/46",
      "E05Y2400/322"
    ],
    "status_code": 30
  },
  {
    "patent_number": "US20250257598A1",
    "title": "LINKAGE FOR A DOOR ACTUATOR",
    "abstract": "",
    "assignee": "dormakaba Deutschland GmbH",
    "inventors": [
      "Thomas SALUTZKI",
      "Sabine WIEMANN",
      "Alexander HELLWIG"
    ],
    "filing_date": "2025-04-29",
    "grant_date": null,
    "cpc_codes": [
      "E05F   3/227",
      "E05F  15/00",
      "E05Y2201/214",
      "E05Y2201/626",
      "E05Y2600/63",
      "E05Y2900/132"
    ],
    "status_code": 30
  },
  {
    "patent_number": "",
    "title": "METHOD FOR OPERATING AN ELECTROMECHANICAL LOCKING DEVICE",
    "abstract": "",
    "assignee": "DORMAKABA SCHWEIZ AG",
    "inventors": [
      "Stephan HANSELMANN",
      "Martin BUHOLZER",
      "Stefan GREIL"
    ],
    "filing_date": "2025-04-16",
    "grant_date": null,
    "cpc_codes": [],
    "status_code": 30
  },
  {
    "patent_number": "",
    "title": "METHOD FOR OPERATING AN ELECTROMECHANICAL LOCKING DEVICE",
    "abstract": "",
    "assignee": "DORMAKABA SCHWEIZ AG",
    "inventors": [
      "Stephan HANSELMANN",
      "Stefan GREIL",
      "Tom MEIER",
      "Tommy BLASER"
    ],
    "filing_date": "2025-04-15",
    "grant_date": null,
    "cpc_codes": [],
    "status_code": 17
  }
]
```
</details>

---

## API Call 3: Search Spectrum Brands patents, filtered to last 2 years

**Endpoint:** `api.uspto.gov/api/v1/patent/applications/search (assignee: Spectrum Brands)`

**Parameters:**
```json
{
  "q": "Spectrum Brands",
  "rows": 100
}
```

**Results:** 25 items returned

<details>
<summary>Preview (first 5 results)</summary>

```json
[
  {
    "patent_number": "",
    "title": "USER INTERFACE FOR AN AIR FILTRATION ASSEMBLY",
    "abstract": "",
    "assignee": "Apex Brands, Inc.",
    "inventors": [
      "Ralf ZERWECK",
      "Michael MOHL"
    ],
    "filing_date": "2025-12-02",
    "grant_date": null,
    "cpc_codes": [],
    "status_code": 30
  },
  {
    "patent_number": "",
    "title": "SPECTRUM UTILIZATION FOR WIRELESS COMMUNICATION",
    "abstract": "",
    "assignee": "ZTE CORPORATION",
    "inventors": [
      "Jing SHI",
      "Xianghui HAN",
      "Xingguang WEI",
      "Shuaihua KOU"
    ],
    "filing_date": "2025-11-11",
    "grant_date": null,
    "cpc_codes": [
      "H04L   5/14",
      "H04L   5/0041",
      "H04W  72/0453"
    ],
    "status_code": 30
  },
  {
    "patent_number": "",
    "title": "Bottle",
    "abstract": "",
    "assignee": "GOOD BRANDS",
    "inventors": [
      "Jules DINAND"
    ],
    "filing_date": "2025-10-09",
    "grant_date": null,
    "cpc_codes": [],
    "status_code": 30
  },
  {
    "patent_number": "",
    "title": "Thickener Composition, Thickened Nutritive Products, Methods For Preparing Thickened Nutritive Products, And Methods For Providing Nutrition",
    "abstract": "",
    "assignee": "Kent Consumer Brands Americas, LLC",
    "inventors": [
      "Douglas A. Stetzer"
    ],
    "filing_date": "2025-10-07",
    "grant_date": null,
    "cpc_codes": [],
    "status_code": 30
  },
  {
    "patent_number": "US20260019925A1",
    "title": "NETWORK-BASED SYSTEMS AND METHODS TO SELECTIVELY ENABLE AND DISABLE CITIZEN BAND RADIO SPECTRUM (CBRS) RADIO FOR INDIVIDUAL USERS",
    "abstract": "",
    "assignee": "AT&T Intellectual Property I, L.P.",
    "inventors": [
      "Howard Lang",
      "Joseph Soryal",
      "Nicholas Thompson",
      "Jasminka Dizdarevic",
      "Marcus Thor"
    ],
    "filing_date": "2025-09-24",
    "grant_date": null,
    "cpc_codes": [
      "H04W  48/08",
      "H04W  48/04",
      "H04W  72/044"
    ],
    "status_code": 30
  }
]
```
</details>

---

## API Call 4: Search Stanley Black & Decker patents, filtered to last 2 years

**Endpoint:** `api.uspto.gov/api/v1/patent/applications/search (assignee: Stanley Black & Decker)`

**Parameters:**
```json
{
  "q": "Stanley Black & Decker",
  "rows": 100
}
```

**Results:** 25 items returned

<details>
<summary>Preview (first 5 results)</summary>

```json
[
  {
    "patent_number": "",
    "title": "PROCESS FOR PREPARING LACTIC ACID",
    "abstract": "",
    "assignee": "CARGILL, INCORPORATED",
    "inventors": [
      "Emily Marie Schmitz Bunch",
      "Christopher Lawrence Frank",
      "Nolan Ray Mente",
      "Joseph Spencer",
      "Eric Stanley Sumner"
    ],
    "filing_date": "2025-11-07",
    "grant_date": null,
    "cpc_codes": [],
    "status_code": 30
  },
  {
    "patent_number": "",
    "title": "WAVELENGTH CONVERSION DEVICE AND ILLUMINATION DEVICE",
    "abstract": "",
    "assignee": "KYOTO UNIVERSITY",
    "inventors": [
      "Yosuke MAEMURA",
      "Ryosuke KAMAKURA",
      "Shunsuke MURAI"
    ],
    "filing_date": "2025-10-20",
    "grant_date": null,
    "cpc_codes": [
      "F21V   9/32",
      "F21Y2115/10",
      "C09K  11/7715"
    ],
    "status_code": 30
  },
  {
    "patent_number": "US20260024788A1",
    "title": "INTEGRATED WASTE REDUCTION SYSTEM",
    "abstract": "",
    "assignee": "Black & Veatch Holding Company",
    "inventors": [
      "Sandeep Sathyamoorthy"
    ],
    "filing_date": "2025-09-26",
    "grant_date": null,
    "cpc_codes": [
      "H01M   8/04186",
      "H01M   8/004",
      "H01M   8/16"
    ],
    "status_code": 30
  },
  {
    "patent_number": "US20260023153A1",
    "title": "ADAPTIVE FAN NOISE SUPPRESSION FOR TRAFFIC RADAR SYSTEMS",
    "abstract": "",
    "assignee": "Applied Concepts, Inc.",
    "inventors": [
      "Stanley A. Walker",
      "Steven F. Hocker",
      "Zhigang Jin",
      "John C. Miller"
    ],
    "filing_date": "2025-09-25",
    "grant_date": null,
    "cpc_codes": [
      "G01S   7/2813"
    ],
    "status_code": 41
  },
  {
    "patent_number": "US20260021266A1",
    "title": "PATIENT INTERFACE SYSTEM",
    "abstract": "",
    "assignee": "Fisher & Paykel Healthcare Limited",
    "inventors": [
      "Leon Tyler STANLEY",
      "Brad Michael HOWARTH",
      "Michael Paul RONAYNE",
      "Samuel Rollo Ross DAVIS",
      "Hemanth PEMMARAJU",
      "Larissa Grace MICHELSEN",
      "Oscar Elliot James McGERTY",
      "Julio Derek MEECH",
      "Amelia Rhian BECKLEY"
    ],
    "filing_date": "2025-09-25",
    "grant_date": null,
    "cpc_codes": [
      "A61M  16/0622",
      "A61M  16/065",
      "A61M  16/0666",
      "A61M  16/16",
      "A61M2205/0216"
    ],
    "status_code": 30
  }
]
```
</details>

---

