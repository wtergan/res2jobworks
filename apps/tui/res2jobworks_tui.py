"""Terminal dashboard renderer over core command envelopes.

This is the MVP TUI surface: a dense, read-only operational view that can be
wrapped by a richer Textual app later without changing domain behavior.
"""

from pathlib import Path

from apps.dashboard_read_model import load_dashboard_jobs


def render_dashboard(database_path: Path | str) -> str:
    """Render the job queue with status, score, and citation preview."""
    jobs_envelope, dashboard_jobs = load_dashboard_jobs(database_path)
    if not jobs_envelope.ok:
        return _errors(jobs_envelope)
    lines = ["res2jobWorks", "Jobs"]
    for dashboard_job in dashboard_jobs:
        job = dashboard_job.summary
        status = job["current_status"] or "untracked"
        score = job["latest_score"] if job["latest_score"] is not None else "-"
        lines.append(f"- {job['title']} | {job['employer']} | {status} | score {score}")
        detail = dashboard_job.detail
        if detail.ok:
            for evaluation in detail.data["evaluations"]:
                lines.append(f"  evaluation: {evaluation['summary']}")
    return "\n".join(lines) + "\n"


def _errors(envelope) -> str:
    return "\n".join(error.message for error in envelope.errors) + "\n"


def main(database_path: str) -> None:
    """Print the local dashboard to stdout."""
    print(render_dashboard(database_path), end="")
