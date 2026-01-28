# API Research Notes

## Sketchfab (NOT USED)
- Download API: https://sketchfab.com/developers/download-api
- Only provides glTF, GLB, USDZ formats
- NOT compatible with Solidworks (needs STEP, IGES)

## GrabCAD (NOT USED)
- No public API for library search/download
- SDK is for 3D printing workflows only

## TraceParts (PENDING API ACCESS)
- Developer portal: https://developers.traceparts.com
- Endpoints:
  - GET /v2/Search/ProductList - search products
  - GET /v3/Product/CadDataAvailability - check formats
  - POST /v3/Product/cadRequest - request download
- Has ASSA ABLOY models directly
- Applied for access (waiting for approval)

## USPTO Patent Data (DEPRECATED)
- USPTO PEDS API (ped.uspto.gov) was RETIRED March 2025
- patent_client library no longer works (uses retired PEDS API)
- New Open Data Portal at data.uspto.gov lacks direct REST API

## Google Patents (SELECTED)
- URL: https://patents.google.com/xhr/query
- No API key required
- Supports:
  - Search by assignee (company)
  - Search by title keywords
  - Get patent details
- Note: May rate-limit automated requests
- Fallback: Sample data for known companies when rate-limited

## Snowflake MCP Tools
- mcp__snowflake__run_snowflake_query
- mcp__snowflake__create_object
- mcp__snowflake__list_objects
- Already connected to user's account
- Working database: SNOWFLAKE_LEARNING_DB

## AWS CLI
- Verified: aws-cli/2.33.2
- Account: 987540640696
- User: kylechalmers-cli
- S3 bucket created: cad-designs-demo
