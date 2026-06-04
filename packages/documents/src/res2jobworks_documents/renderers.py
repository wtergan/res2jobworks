"""Local document renderers that keep generated files as artifacts."""

from __future__ import annotations

import io
import zipfile
from html import escape
from pathlib import Path
from uuid import uuid4

from res2jobworks_core.commands._support import validate_output_path
from res2jobworks_core.repositories.sqlite import SQLiteRepository
from res2jobworks_documents.drafting import DocumentDraft


def render_markdown_document(draft: DocumentDraft) -> str:
    """Render a draft as inspectable Markdown with provenance metadata."""
    lines = [f"# {draft.title}", "", draft.body, "", "## Provenance"]
    for link in draft.evidence:
        lines.append(f"- {link.source_table}:{link.source_id} — {link.quote}")
    if draft.unsupported_inferences:
        lines.extend(["", "## Unsupported Inferences"])
        for inference in draft.unsupported_inferences:
            lines.append(f"- {inference}")
    lines.extend(["", f"Review state: {draft.review_state}", ""])
    return "\n".join(lines)


def render_docx_document(draft: DocumentDraft) -> bytes:
    """Render a minimal DOCX artifact using stdlib Office Open XML."""
    document_xml = _document_xml(render_markdown_document(draft).splitlines())
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            (
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<Types xmlns="http://schemas.openxmlformats.org/package/2006/'
                'content-types">'
                '<Default Extension="rels" ContentType="application/vnd.'
                'openxmlformats-package.relationships+xml"/>'
                '<Default Extension="xml" ContentType="application/xml"/>'
                '<Override PartName="/word/document.xml" '
                'ContentType="application/vnd.openxmlformats-officedocument.'
                'wordprocessingml.document.main+xml"/>'
                "</Types>"
            ),
        )
        archive.writestr(
            "_rels/.rels",
            (
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/'
                'package/2006/relationships">'
                '<Relationship Id="rId1" '
                'Type="http://schemas.openxmlformats.org/officeDocument/'
                '2006/relationships/officeDocument" '
                'Target="word/document.xml"/>'
                "</Relationships>"
            ),
        )
        archive.writestr("word/document.xml", document_xml)
    return output.getvalue()


def render_pdf_document(draft: DocumentDraft) -> bytes:
    """Render a simple single-page text PDF artifact."""
    text = render_markdown_document(draft)
    lines = [_pdf_escape(line[:100]) for line in text.splitlines()[:45]]
    content_lines = ["BT", "/F1 10 Tf", "50 780 Td"]
    for index, line in enumerate(lines):
        if index:
            content_lines.append("0 -14 Td")
        content_lines.append(f"({line}) Tj")
    content_lines.append("ET")
    stream = "\n".join(content_lines).encode("latin-1", errors="replace")
    page = (
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
    )
    contents = (
        b"<< /Length "
        + str(len(stream)).encode("ascii")
        + b" >>\nstream\n"
        + stream
        + b"\nendstream"
    )
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        page,
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        contents,
    ]
    return _pdf(objects)


def render_document_artifact(
    database_path: Path | str,
    *,
    draft: DocumentDraft,
    output_path: Path | str,
    format: str,
    target_table: str,
    target_id: str,
) -> dict:
    """Write a generated document and record it as a derived export artifact."""
    path = validate_output_path(output_path)
    content = _render_by_format(draft, format)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
    if isinstance(content, bytes):
        temporary_path.write_bytes(content)
    else:
        temporary_path.write_text(content, encoding="utf-8")
    repository = SQLiteRepository(database_path)
    try:
        export_record = repository.record_export(
            export_id=f"document-{draft.kind}-{path.stem}-{uuid4().hex}",
            export_type=f"{draft.kind}_document",
            format=format,
            target_table=target_table,
            target_id=target_id,
            path=str(path),
            metadata={
                "document_kind": draft.kind,
                "review_state": draft.review_state,
                "evidence_count": len(draft.evidence),
                "unsupported_inference_count": len(draft.unsupported_inferences),
            },
        )
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise
    temporary_path.replace(path)
    return export_record


def _render_by_format(draft: DocumentDraft, format: str) -> str | bytes:
    if format == "markdown":
        return render_markdown_document(draft)
    if format == "docx":
        return render_docx_document(draft)
    if format == "pdf":
        return render_pdf_document(draft)
    raise ValueError("document format must be markdown, docx, or pdf")


def _document_xml(lines: list[str]) -> str:
    paragraphs = "".join(
        f"<w:p><w:r><w:t>{escape(line)}</w:t></w:r></w:p>" for line in lines
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{paragraphs}</w:body></w:document>"
    )


def _pdf_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _pdf(objects: list[bytes]) -> bytes:
    output = io.BytesIO()
    output.write(b"%PDF-1.4\n")
    offsets = [0]
    for index, body in enumerate(objects, start=1):
        offsets.append(output.tell())
        output.write(f"{index} 0 obj\n".encode("ascii"))
        output.write(body)
        output.write(b"\nendobj\n")
    xref = output.tell()
    output.write(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.write(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.write(
        (
            "trailer\n"
            f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            "startxref\n"
            f"{xref}\n"
            "%%EOF\n"
        ).encode("ascii")
    )
    return output.getvalue()
