"""Static local web dashboard rendered from core command envelopes.

The web client is intentionally server-thin for MVP 1: it reads canonical
SQLite state through core query commands and returns inspectable HTML that can
be served by any local HTTP wrapper without duplicating product behavior.
"""

from html import escape
from pathlib import Path

from res2jobworks_core.commands import list_jobs, show_job
from res2jobworks_core.contracts import CommandEnvelope


def render_dashboard_html(database_path: Path | str) -> str:
    """Render the local job dashboard as responsive, semantic HTML."""
    jobs_envelope = list_jobs(database_path)
    if not jobs_envelope.ok:
        return _document(title="res2jobWorks", body=_error_region(jobs_envelope))

    jobs = jobs_envelope.data["jobs"]
    rows = "\n".join(_job_row(job) for job in jobs)
    details = "\n".join(_job_detail(database_path, job["id"]) for job in jobs)
    empty_state = (
        '<p class="empty">No jobs imported yet.</p>'
        if not jobs
        else ""
    )
    body = f"""
<a class="skip-link" href="#main">Skip to main content</a>
<main id="main" class="shell">
  <header class="masthead">
    <p class="eyebrow" translate="no">res2jobWorks</p>
    <h1>Evaluation Tracker</h1>
  </header>
  <section aria-labelledby="jobs-heading" class="panel">
    <div class="section-heading">
      <h2 id="jobs-heading">Jobs</h2>
      <p>{len(jobs)} tracked</p>
    </div>
    {empty_state}
    <div class="table-wrap" role="region" aria-label="Tracked jobs" tabindex="0">
      <table>
        <thead>
          <tr>
            <th scope="col">Job</th>
            <th scope="col">Employer</th>
            <th scope="col">Status</th>
            <th scope="col">Score</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
  </section>
  <section aria-labelledby="details-heading" class="details">
    <h2 id="details-heading">Evidence</h2>
    {details}
  </section>
</main>
"""
    return _document(title="res2jobWorks Evaluation Tracker", body=body)


def _job_row(job: dict) -> str:
    status = job["current_status"] or "untracked"
    score = _score(job["latest_score"])
    return f"""
<tr>
  <th scope="row">{escape(job["title"])}</th>
  <td>{escape(job["employer"])}</td>
  <td><span class="status">{escape(status)}</span></td>
  <td class="number">{score}</td>
</tr>
"""


def _job_detail(database_path: Path | str, job_id: str) -> str:
    detail = show_job(database_path, job_id=job_id)
    if not detail.ok:
        return _error_region(detail)
    job = detail.data["job"]
    evaluations = detail.data["evaluations"]
    applications = detail.data["applications"]
    evaluation_blocks = "\n".join(_evaluation_block(item) for item in evaluations)
    status = applications[-1]["current_status"] if applications else "untracked"
    if not evaluation_blocks:
        evaluation_blocks = '<p class="empty">No evaluations recorded.</p>'
    return f"""
<article class="job-detail">
  <h3>{escape(job["title"])}</h3>
  <p class="meta">{escape(job["employer"])} · <span>{escape(status)}</span></p>
  {evaluation_blocks}
</article>
"""


def _evaluation_block(evaluation: dict) -> str:
    citations = "\n".join(
        _citation_line(citation) for citation in evaluation["citations"]
    )
    return f"""
<section class="evaluation" aria-label="Evaluation summary">
  <div class="score">
    <span>Score</span>
    <strong>{_score(evaluation["score"])}</strong>
  </div>
  <p>{escape(evaluation["summary"])}</p>
  <ul>
    {citations}
  </ul>
</section>
"""


def _citation_line(citation: dict) -> str:
    source_type = (
        citation.get("source_type") or citation.get("source_table") or "source"
    )
    source_id = citation.get("source_id") or citation.get("id") or "unknown"
    label = f"{source_type} {source_id}"
    quote = (
        citation.get("quote")
        or citation.get("reason")
        or citation.get("rationale")
        or ""
    )
    return f"<li><b>{escape(label)}</b>: {escape(quote)}</li>"


def _error_region(envelope: CommandEnvelope) -> str:
    messages = " ".join(error.message for error in envelope.errors)
    return f'<section role="alert" class="error">{escape(messages)}</section>'


def _score(value: object) -> str:
    return "-" if value is None else escape(str(value))


def _document(*, title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f8f5;
      --surface: #ffffff;
      --text: #17201b;
      --muted: #5d695f;
      --line: #d7ddd6;
      --accent: #1c6b5a;
      --accent-soft: #e4f1ec;
      --warning: #7a4d00;
    }}
    * {{ box-sizing: border-box; }}
    html {{ background: var(--bg); color: var(--text); }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system,
        BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 1rem;
      line-height: 1.45;
      -webkit-tap-highlight-color: rgba(28, 107, 90, 0.18);
    }}
    .skip-link {{
      left: 1rem;
      position: absolute;
      top: -4rem;
      z-index: 10;
    }}
    .skip-link:focus-visible {{
      background: var(--accent);
      color: white;
      outline: 0.2rem solid var(--text);
      padding: 0.75rem 1rem;
      top: 1rem;
    }}
    .shell {{
      margin: 0 auto;
      max-width: 72rem;
      padding: max(1rem, env(safe-area-inset-top)) 1rem 2rem;
    }}
    .masthead {{
      border-bottom: 1px solid var(--line);
      padding: 1.25rem 0 1rem;
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0;
      margin: 0 0 0.25rem;
      text-transform: uppercase;
    }}
    h1, h2, h3 {{ margin: 0; text-wrap: balance; }}
    h1 {{ font-size: 2rem; line-height: 1.05; }}
    h2 {{ font-size: 1.15rem; }}
    h3 {{ font-size: 1rem; }}
    .panel, .job-detail {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 0.5rem;
    }}
    .panel {{ margin-top: 1rem; overflow: hidden; }}
    .section-heading {{
      align-items: center;
      display: flex;
      gap: 1rem;
      justify-content: space-between;
      padding: 1rem;
    }}
    .section-heading p, .meta, .empty {{ color: var(--muted); margin: 0; }}
    .empty {{ padding: 1rem; }}
    .table-wrap {{
      overflow-x: auto;
      scroll-margin-top: 1rem;
    }}
    .table-wrap:focus-visible {{
      outline: 0.2rem solid var(--accent);
      outline-offset: -0.2rem;
    }}
    table {{
      border-collapse: collapse;
      min-width: 42rem;
      width: 100%;
    }}
    th, td {{
      border-top: 1px solid var(--line);
      padding: 0.85rem 1rem;
      text-align: left;
      vertical-align: top;
    }}
    th {{ font-weight: 700; }}
    td, th {{ overflow-wrap: anywhere; }}
    .number {{ font-variant-numeric: tabular-nums; }}
    .status {{
      background: var(--accent-soft);
      border-radius: 999px;
      color: var(--accent);
      display: inline-block;
      font-weight: 700;
      padding: 0.2rem 0.55rem;
    }}
    .details {{
      display: grid;
      gap: 0.75rem;
      margin-top: 1.25rem;
    }}
    .job-detail {{ padding: 1rem; }}
    .meta {{ margin-top: 0.25rem; }}
    .evaluation {{
      border-top: 1px solid var(--line);
      display: grid;
      gap: 0.75rem;
      margin-top: 1rem;
      padding-top: 1rem;
    }}
    .evaluation p, .evaluation ul {{ margin: 0; }}
    .evaluation ul {{
      display: grid;
      gap: 0.5rem;
      padding-left: 1.25rem;
    }}
    .score {{
      align-items: baseline;
      display: flex;
      gap: 0.5rem;
    }}
    .score span {{ color: var(--muted); }}
    .score strong {{ color: var(--accent); font-size: 1.35rem; }}
    .error {{
      background: #fff6dd;
      border: 1px solid #e5bd63;
      border-radius: 0.5rem;
      color: var(--warning);
      padding: 1rem;
    }}
    @media (min-width: 48rem) {{
      .shell {{ padding-inline: 1.5rem; }}
      h1 {{ font-size: 2.6rem; }}
      .details {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .details > h2 {{ grid-column: 1 / -1; }}
    }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""
