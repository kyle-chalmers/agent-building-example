# Planning Context & Decision Log

## Original Request
Build an agent demo for ASSA ABLOY that demonstrates:
1. API integration for CAD/design search
2. Snowflake database for metadata storage
3. S3/local storage for downloaded files

## Key Decisions

### Decision 1: Sketchfab → GrabCAD → TraceParts → USPTO Patents → Google Patents
- **Sketchfab**: Only offers glTF/GLB formats - not Solidworks compatible
- **GrabCAD**: No public API for library access
- **TraceParts**: Has API but requires approval (not available for tomorrow's demo)
- **USPTO PEDS**: Retired March 2025 (ped.uspto.gov no longer resolves)
- **Google Patents**: Free, no API key, relevant to ASSA ABLOY (competitive intelligence)

### Decision 2: Snowflake-First Architecture
- Query Snowflake before making external API calls
- Cache results to avoid redundant API calls
- Enables fast repeat queries and trend analysis

### Decision 3: Local Markdown Reports (not S3)
- Easier to demo and share
- No AWS setup complexity
- Professional format for stakeholders

### Decision 4: Agent Best Practices
- Slim CLAUDE.md (only actionable instructions)
- Modular skills with tool restrictions
- Subagent for isolated research tasks

### Decision 5: Snowflake Database
- Originally planned: ANALYTICS.PATENT_INTELLIGENCE
- Actual: SNOWFLAKE_LEARNING_DB.PATENT_INTELLIGENCE (permissions)

## Tools & Services Used
- **Google Patents API** (no API key needed, fallback sample data for rate limits)
- **Snowflake CLI (snow)** for database operations
- **Snowflake MCP tools** (already connected)
- **AWS CLI** (verified working, bucket: s3://cad-designs-demo)
- **Claude Code** slash commands

## Workshop Talking Points
1. How we adapted when first choice (Sketchfab) didn't fit
2. Snowflake-first pattern for efficient caching
3. Best practices for agent configuration
4. Modular skill design
