"""Terminal dashboard renderer over core command envelopes.

This is the MVP TUI surface: a dense, read-only operational view that can be
wrapped by a richer Textual app later without changing domain behavior.
"""

from pathlib import Path

from apps.dashboard_read_model import load_dashboard_jobs
from res2jobworks_automation import review_state_label, strip_control_characters


def render_dashboard(database_path: Path | str) -> str:
    """Render the job queue with status, score, and citation preview."""
    jobs_envelope, dashboard_jobs = load_dashboard_jobs(database_path)
    if not jobs_envelope.ok:
        return _errors(jobs_envelope)
    lines = ["res2jobWorks", "Jobs"]
    for dashboard_job in dashboard_jobs:
        job = dashboard_job.summary
        title = _terminal_text(job["title"])
        employer = _terminal_text(job["employer"])
        status = _terminal_text(job["current_status"] or "untracked")
        score = job["latest_score"] if job["latest_score"] is not None else "-"
        lines.append(f"- {title} | {employer} | {status} | score {score}")
        detail = dashboard_job.detail
        if detail.ok:
            for source in detail.data["job_sources"]:
                source_label = _terminal_text(source["source_url"] or source["title"])
                review_state = _terminal_text(
                    review_state_label(source["metadata"].get("review_state"))
                )
                suffix = f" | {review_state}" if review_state else ""
                lines.append(f"  source: {source_label}{suffix}")
            for evaluation in detail.data["evaluations"]:
                lines.append(f"  evaluation: {_terminal_text(evaluation['summary'])}")
    return "\n".join(lines) + "\n"


def _terminal_text(value: object) -> str:
    return strip_control_characters(str(value))


def _errors(envelope) -> str:
    return "\n".join(_terminal_text(error.message) for error in envelope.errors) + "\n"


def main(database_path: str) -> None:
    """Print the local dashboard to stdout."""
    print(render_dashboard(database_path), end="")
