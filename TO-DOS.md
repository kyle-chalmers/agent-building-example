# TO-DOS

## Completed

### ✅ Integrate USPTO Open Data Portal API - 2026-01-27

**Status:** COMPLETE

**Solution found:**
- Correct API endpoint: `https://api.uspto.gov/api/v1/patent/applications/search`
- Auth header: `X-API-KEY: <key>`
- Query param: `?q=<search_term>&rows=<limit>`

**Changes made:**
1. Updated `patent_client_wrapper.py` - USPTO ODP as primary, Google Patents as fallback
2. Updated `.env.example` - API key documentation
3. Updated `CLAUDE.md` - Available tools section for agents

**Results:**
- Allegion: 41 patents
- Dormakaba: 413 patents
- Total database: 12.6M+ patent applications

---

## Pending

_No pending items_
