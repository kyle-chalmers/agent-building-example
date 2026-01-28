# Patent Intelligence Agent

An intelligent agent for competitive patent analysis. Template for a company that does [ENTER TYPE OF WORK].

## Features
- Search USPTO patents by company or technology keywords
- Cache results in Snowflake for fast repeat queries
- Generate markdown reports for stakeholders
- Natural language interface via Claude Code

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment (optional - for direct Snowflake access)
cp .env.example .env
# Edit .env with your Snowflake credentials

# Launch with Claude Code
claude
```

Then ask: *"Find the latest patents filed by a competitor"*

## Demo Flow

### 1. Show the Configuration
Open `CLAUDE.md` to show how the agent understands your competitive landscape.

### 2. Natural Language Search
Ask: *"Find recent smart lock patents from Allegion"*
- Agent checks Snowflake first (cache)
- Falls back to USPTO API if needed
- Stores results automatically

### 3. Generate Competitor Report
Run: `/competitor-report Allegion`
- Creates markdown report in `./reports/`
- Includes filing trends, key inventors, technology focus

### 4. Analyze Trends
Run: `/patent-trends`
- Aggregates data from Snowflake
- Shows competitive landscape over time

### 5. Key Talking Points
- **No API keys needed** - Uses public USPTO data
- **Snowflake caching** - Fast repeat queries
- **Local reports** - Easy to share markdown files
- **Extensible** - Can add European patents, more competitors

## Slash Commands

| Command | Description |
|---------|-------------|
| `/patent-search <query>` | Search patents by company or keywords |
| `/competitor-report <company>` | Generate competitor analysis report |
| `/patent-trends [technology]` | Analyze filing trends |

## Architecture

```
User Query → Claude Code → Check Snowflake
                              ↓
                         Cache Hit? → Return Results
                              ↓ No
                         USPTO API → Store in Snowflake → Return Results
```

## Competitors Tracked

Configure in `tools/__init__.py`:
```python
COMPETITORS = [
    "Competitor A",
    "Competitor B",
    # Add your competitors here
]
```

## Technologies of Interest

Configure in `tools/__init__.py`:
```python
TECHNOLOGIES = [
    "keyword 1",
    "keyword 2",
    # Add your technology keywords here
]
```

## Project Structure
```
├── CLAUDE.md                 # Agent configuration
├── patent_client_wrapper.py  # USPTO API wrapper
├── patent_agent.py           # Core agent logic
├── demo.py                   # Interactive demo script
├── reports/                  # Generated reports
├── .planning/                # Workshop documentation
└── .claude/
    ├── agents/               # Subagent definitions
    └── commands/             # Slash commands
```

## Snowflake Database
- **Database**: SNOWFLAKE_LEARNING_DB
- **Schema**: PATENT_INTELLIGENCE
- **Table**: PATENTS

## Requirements
- Python 3.11+
- Snowflake account (for caching)
- Claude Code CLI

## Running Tests

```bash
# Unit tests only
pytest tests/ -v -m "not integration"

# All tests including live API
pytest tests/ -v
```

## License
Demo project - configure for your company
