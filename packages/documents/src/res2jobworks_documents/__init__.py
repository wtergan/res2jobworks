"""Evidence-backed tailoring and document rendering for phase 2.

The package reads canonical SQLite records through core repository contracts and
creates reviewable draft artifacts. It does not mutate profile/job truth or
invent unsupported claims.
"""

from res2jobworks_documents.commands import (
    draft_application_answer,
    draft_cover_letter,
    render_cover_letter,
    suggest_tailoring,
)
from res2jobworks_documents.drafting import (
    build_application_answer_draft,
    build_cover_letter_draft,
    build_resume_diff,
    build_tailoring_suggestions,
)
from res2jobworks_documents.evidence import EvidenceBundle, EvidenceLink, load_evidence
from res2jobworks_documents.readiness import analyze_document_readiness
from res2jobworks_documents.renderers import (
    render_document_artifact,
    render_docx_document,
    render_markdown_document,
    render_pdf_document,
)

__all__ = [
    "EvidenceBundle",
    "EvidenceLink",
    "analyze_document_readiness",
    "build_application_answer_draft",
    "build_cover_letter_draft",
    "build_resume_diff",
    "build_tailoring_suggestions",
    "draft_application_answer",
    "draft_cover_letter",
    "load_evidence",
    "render_cover_letter",
    "render_docx_document",
    "render_document_artifact",
    "render_markdown_document",
    "render_pdf_document",
    "suggest_tailoring",
]
