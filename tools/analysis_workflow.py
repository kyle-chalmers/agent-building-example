"""Analysis workflow system for patent intelligence.

Creates timestamped analysis folders with full audit trail:
- metadata.json: Request details, timestamps, parameters
- 01_snowflake_queries.md: All Snowflake queries executed
- 02_api_results.md: Raw USPTO/Google Patents API results
- 03_analysis.md: Intermediate analysis/filtering steps
- 04_report.md: Final formatted report

Example folder structure:
    analysis/
    └── 2026-01-28_smart-lock-patents/
        ├── metadata.json
        ├── 01_snowflake_queries.md
        ├── 02_api_results.md
        ├── 03_analysis.md
        └── 04_report.md
"""
import json
import os
import re
from datetime import datetime
from typing import Optional


def _slugify(text: str, max_length: int = 50) -> str:
    """Convert text to URL-friendly slug.

    Args:
        text: Text to slugify
        max_length: Maximum length of slug

    Returns:
        Lowercase slug with hyphens
    """
    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:max_length].rstrip('-')


class AnalysisWorkflow:
    """Manages an analysis session with full audit trail.

    Creates a timestamped folder containing:
    - metadata.json with request context
    - Markdown files logging each step

    Usage:
        workflow = AnalysisWorkflow("Analyze smart lock patents from 2024")
        workflow.log_snowflake_query("SELECT * FROM ...", results)
        workflow.log_api_call("USPTO", {"q": "smart lock"}, results)
        workflow.log_analysis("Filtering by date", {"filtered_count": 47})
        workflow.write_report("# Smart Lock Analysis\\n...")
        workflow.finalize()
    """

    def __init__(
        self,
        request: str,
        jira_ticket: Optional[str] = None,
        jira_url: Optional[str] = None,
        base_dir: str = "analysis"
    ):
        """Initialize a new analysis workflow session.

        Args:
            request: The analysis request/question
            jira_ticket: Optional Jira ticket ID (e.g., "PATENT-456")
            jira_url: Optional full Jira URL
            base_dir: Base directory for analysis folders (default: "analysis")
        """
        self.request = request
        self.jira_ticket = jira_ticket
        self.jira_url = jira_url
        self.base_dir = base_dir
        self.started_at = datetime.utcnow()

        # Create folder name
        date_str = self.started_at.strftime("%Y-%m-%d")
        slug = _slugify(request)

        if jira_ticket:
            folder_name = f"{jira_ticket}_{slug}"
        else:
            folder_name = f"{date_str}_{slug}"

        self.session_dir = os.path.join(base_dir, folder_name)

        # Initialize metadata
        self.metadata = {
            "request": request,
            "jira_ticket": jira_ticket,
            "jira_url": jira_url,
            "started_at": self.started_at.isoformat() + "Z",
            "completed_at": None,
            "status": "in_progress",
            "snowflake_query_count": 0,
            "api_call_count": 0,
            "analysis_step_count": 0,
        }

        # Create directory and initialize files
        self._setup_session()

    def _setup_session(self) -> None:
        """Create session directory and initialize markdown files."""
        os.makedirs(self.session_dir, exist_ok=True)

        # Initialize markdown files with headers
        self._write_file("01_snowflake_queries.md", "# Snowflake Queries Executed\n\n")
        self._write_file("02_api_results.md", "# USPTO/Google Patents API Calls\n\n")
        self._write_file("03_analysis.md", "# Analysis Steps\n\n")
        self._write_file("04_report.md", "")  # Report written at end

        # Write initial metadata
        self._write_metadata()

    def _write_file(self, filename: str, content: str, append: bool = False) -> None:
        """Write content to a file in the session directory.

        Args:
            filename: Name of file
            content: Content to write
            append: If True, append to existing file
        """
        filepath = os.path.join(self.session_dir, filename)
        mode = "a" if append else "w"
        with open(filepath, mode) as f:
            f.write(content)

    def _write_metadata(self) -> None:
        """Write current metadata to metadata.json."""
        filepath = os.path.join(self.session_dir, "metadata.json")
        with open(filepath, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def log_snowflake_query(
        self,
        query: str,
        results: list,
        description: Optional[str] = None
    ) -> None:
        """Log a Snowflake query and its results.

        Args:
            query: SQL query that was executed
            results: List of result rows
            description: Optional description of query purpose
        """
        self.metadata["snowflake_query_count"] += 1
        query_num = self.metadata["snowflake_query_count"]

        content = f"## Query {query_num}"
        if description:
            content += f": {description}"
        content += "\n\n"
        content += f"```sql\n{query.strip()}\n```\n\n"
        content += f"**Results:** {len(results)} rows\n\n"

        if results:
            # Show first few results as preview
            preview = results[:5]
            content += "<details>\n<summary>Preview (first 5 rows)</summary>\n\n"
            content += "```json\n"
            content += json.dumps(preview, indent=2, default=str)
            content += "\n```\n</details>\n\n"

        content += "---\n\n"

        self._write_file("01_snowflake_queries.md", content, append=True)
        self._write_metadata()

    def log_api_call(
        self,
        endpoint: str,
        params: dict,
        results: list,
        description: Optional[str] = None
    ) -> None:
        """Log an API call and its results.

        Args:
            endpoint: API endpoint URL or name
            params: Request parameters
            results: List of results
            description: Optional description
        """
        self.metadata["api_call_count"] += 1
        call_num = self.metadata["api_call_count"]

        content = f"## API Call {call_num}"
        if description:
            content += f": {description}"
        content += "\n\n"
        content += f"**Endpoint:** `{endpoint}`\n\n"
        content += f"**Parameters:**\n```json\n{json.dumps(params, indent=2)}\n```\n\n"
        content += f"**Results:** {len(results)} items returned\n\n"

        if results:
            # Show first few results as preview
            preview = results[:5]
            content += "<details>\n<summary>Preview (first 5 results)</summary>\n\n"
            content += "```json\n"
            content += json.dumps(preview, indent=2, default=str)
            content += "\n```\n</details>\n\n"

        content += "---\n\n"

        self._write_file("02_api_results.md", content, append=True)
        self._write_metadata()

    def log_analysis(
        self,
        step: str,
        data: dict,
        notes: Optional[str] = None
    ) -> None:
        """Log an analysis step.

        Args:
            step: Description of the analysis step
            data: Data/results from this step (as dict for structured logging)
            notes: Optional additional notes
        """
        self.metadata["analysis_step_count"] += 1
        step_num = self.metadata["analysis_step_count"]

        content = f"## Step {step_num}: {step}\n\n"

        if notes:
            content += f"{notes}\n\n"

        # Format data nicely
        if isinstance(data, dict):
            # Try to render as table if it looks like tabular data
            if all(isinstance(v, (int, str, float)) for v in data.values()):
                content += "| Key | Value |\n|-----|-------|\n"
                for k, v in data.items():
                    content += f"| {k} | {v} |\n"
            else:
                content += "```json\n"
                content += json.dumps(data, indent=2, default=str)
                content += "\n```\n"
        else:
            content += f"```\n{data}\n```\n"

        content += "\n---\n\n"

        self._write_file("03_analysis.md", content, append=True)
        self._write_metadata()

    def write_report(self, report: str) -> None:
        """Write the final report.

        Args:
            report: Full markdown report content
        """
        self._write_file("04_report.md", report)

    def finalize(self, status: str = "complete") -> str:
        """Finalize the analysis session.

        Args:
            status: Final status ("complete", "partial", "error")

        Returns:
            Path to the session directory
        """
        self.metadata["completed_at"] = datetime.utcnow().isoformat() + "Z"
        self.metadata["status"] = status
        self._write_metadata()

        return self.session_dir

    @property
    def folder_path(self) -> str:
        """Get the session folder path."""
        return self.session_dir


def create_session_dir(request: str, jira_ticket: Optional[str] = None) -> str:
    """Create a new analysis session directory (convenience function).

    Args:
        request: The analysis request
        jira_ticket: Optional Jira ticket ID

    Returns:
        Path to created directory
    """
    workflow = AnalysisWorkflow(request, jira_ticket=jira_ticket)
    return workflow.session_dir


def generate_report_markdown(
    title: str,
    patents: list[dict],
    analysis: Optional[str] = None
) -> str:
    """Generate markdown report from patent data.

    Args:
        title: Report title
        patents: List of patent dictionaries
        analysis: Optional analysis text to include

    Returns:
        Markdown formatted report string
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    # Count by assignee
    assignee_counts = {}
    for p in patents:
        assignee = p.get("assignee", "Unknown")
        assignee_counts[assignee] = assignee_counts.get(assignee, 0) + 1

    top_assignees = sorted(assignee_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # Find date range
    dates = [p["filing_date"] for p in patents if p.get("filing_date")]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    report = f"""# Patent Report: {title}
Generated: {timestamp}

## Summary
- Total patents found: {len(patents)}
- Date range: {date_range}
- Top assignees: {', '.join([f"{a[0]} ({a[1]})" for a in top_assignees])}

## Patents

"""
    for p in patents[:20]:  # Limit to 20 in report
        report += f"""### {p.get('patent_number', 'N/A')}: {p.get('title', 'Untitled')}
- **Assignee**: {p.get('assignee', 'Unknown')}
- **Filed**: {p.get('filing_date', 'N/A')}
- **Abstract**: {(p.get('abstract') or 'No abstract available')[:300]}...

"""

    if analysis:
        report += f"""## Analysis
{analysis}
"""

    return report
