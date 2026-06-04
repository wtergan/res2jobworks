"""Command-line surface that dispatches to core command handlers.

The CLI owns argument parsing and presentation only. Every mutation and read
returns a `CommandEnvelope` produced by core workflows.
"""

import argparse
import json
import sys
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

from res2jobworks_automation import (
    capture_job,
    capture_text,
    prepare_fill_review,
)
from res2jobworks_core.commands import (
    add_application,
    evaluate_job,
    export_applications,
    import_job,
    import_profile,
    init_workspace,
    list_applications,
    list_jobs,
    show_job,
    show_profile,
    update_application,
)
from res2jobworks_core.contracts import CommandEnvelope, CommandError
from res2jobworks_documents import (
    draft_application_answer,
    draft_cover_letter,
    render_cover_letter,
    suggest_tailoring,
)

CommandHandler = Callable[[Mapping[str, str]], CommandEnvelope]


def main(argv: Sequence[str] | None = None) -> int:
    """Run the res2jobWorks CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    envelope = args.handler(args)
    if args.json:
        print(json.dumps(envelope.model_dump(mode="json"), indent=2, sort_keys=True))
    else:
        print(_human_summary(envelope))
    return 0 if envelope.ok else 1


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser from the stable implemented command surface."""
    parser = argparse.ArgumentParser(prog="res2jobworks")
    parser.add_argument(
        "--json",
        action="store_true",
        help="print command envelope JSON",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    _add_run(subparsers)
    _add_workspace_init(subparsers)
    _add_profile_import(subparsers)
    _add_profile_show(subparsers)
    _add_job_import(subparsers)
    _add_job_evaluate(subparsers)
    _add_jobs_list(subparsers)
    _add_jobs_show(subparsers)
    _add_application_add(subparsers)
    _add_application_update(subparsers)
    _add_application_list(subparsers)
    _add_application_export(subparsers)
    return parser


def _set_handler(
    parser: argparse.ArgumentParser,
    handler: Callable[[argparse.Namespace], CommandEnvelope],
) -> None:
    parser.set_defaults(handler=handler)


def _add_run(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("run")
    parser.add_argument("command_id")
    parser.add_argument(
        "--json",
        action="store_true",
        help="print command envelope JSON",
    )
    parser.add_argument(
        "--input",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="command input. Repeat for multiple inputs.",
    )
    _set_handler(parser, lambda args: _run_command(args.command_id, args.input))


def _add_workspace_init(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("workspace.init")
    parser.add_argument("--workspace-path", required=True)
    _set_handler(parser, lambda args: init_workspace(Path(args.workspace_path)))


def _add_profile_import(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("profile.import")
    _database_arg(parser)
    parser.add_argument("--source-path", default=None)
    parser.add_argument("--source-text", default=None)
    parser.add_argument("--source-type", default="yaml")
    _set_handler(
        parser,
        lambda args: import_profile(
            Path(args.database_path),
            source_path=Path(args.source_path) if args.source_path else None,
            source_text=args.source_text,
            source_type=args.source_type,
        ),
    )


def _add_profile_show(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("profile.show")
    _database_arg(parser)
    parser.add_argument("--profile-id", required=True)
    _set_handler(
        parser,
        lambda args: show_profile(Path(args.database_path), profile_id=args.profile_id),
    )


def _add_job_import(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("jobs.import")
    _database_arg(parser)
    parser.add_argument("--source-path", default=None)
    parser.add_argument("--source-text", default=None)
    parser.add_argument("--source-type", default="markdown")
    _set_handler(
        parser,
        lambda args: import_job(
            Path(args.database_path),
            source_path=Path(args.source_path) if args.source_path else None,
            source_text=args.source_text,
            source_type=args.source_type,
        ),
    )


def _add_job_evaluate(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("jobs.evaluate")
    _database_arg(parser)
    parser.add_argument("--profile-id", required=True)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--rubric-id", default=None)
    _set_handler(
        parser,
        lambda args: evaluate_job(
            Path(args.database_path),
            profile_id=args.profile_id,
            job_id=args.job_id,
            rubric_id=args.rubric_id,
        ),
    )


def _add_jobs_list(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("jobs.list")
    _database_arg(parser)
    _set_handler(parser, lambda args: list_jobs(Path(args.database_path)))


def _add_jobs_show(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("jobs.show")
    _database_arg(parser)
    parser.add_argument("--job-id", required=True)
    _set_handler(
        parser,
        lambda args: show_job(Path(args.database_path), job_id=args.job_id),
    )


def _add_application_add(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("applications.add")
    _database_arg(parser)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--status", default="interested")
    parser.add_argument("--evaluation-id", default=None)
    _set_handler(
        parser,
        lambda args: add_application(
            Path(args.database_path),
            job_id=args.job_id,
            status=args.status,
            evaluation_id=args.evaluation_id,
        ),
    )


def _add_application_update(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("applications.update")
    _database_arg(parser)
    parser.add_argument("--application-id", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--note", default="")
    _set_handler(
        parser,
        lambda args: update_application(
            Path(args.database_path),
            application_id=args.application_id,
            status=args.status,
            note=args.note,
        ),
    )


def _add_application_list(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("applications.list")
    _database_arg(parser)
    _set_handler(parser, lambda args: list_applications(Path(args.database_path)))


def _add_application_export(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("applications.export")
    _database_arg(parser)
    parser.add_argument("--format", required=True, choices=["markdown", "csv"])
    parser.add_argument("--output-path", required=True)
    _set_handler(
        parser,
        lambda args: export_applications(
            Path(args.database_path),
            output_path=Path(args.output_path),
            format=args.format,
        ),
    )


def _database_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--database-path", required=True)


def _human_summary(envelope: CommandEnvelope) -> str:
    if not envelope.ok:
        return "\n".join(error.message for error in envelope.errors)
    if envelope.files:
        return f"{envelope.command}: ok -> {', '.join(envelope.files)}"
    return f"{envelope.command}: ok"


def _run_command(command_id: str, raw_inputs: Sequence[str]) -> CommandEnvelope:
    inputs = _parse_inputs(raw_inputs)
    handler = _RUNNERS.get(command_id)
    if handler is None:
        return CommandEnvelope.failure(
            command_id,
            inputs=inputs,
            errors=[
                CommandError(
                    code="unknown_command",
                    message=(
                        "command is not available through this runner: "
                        f"{command_id}"
                    ),
                )
            ],
        )
    try:
        return handler(inputs)
    except ValueError as exc:
        return CommandEnvelope.failure(
            command_id,
            inputs=inputs,
            errors=[
                CommandError(
                    code="validation_error",
                    message=str(exc),
                )
            ],
        )


def _parse_inputs(raw_inputs: Sequence[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for raw_input in raw_inputs:
        if "=" not in raw_input:
            raise SystemExit(f"--input must use KEY=VALUE format: {raw_input}")
        key, value = raw_input.split("=", 1)
        if not key:
            raise SystemExit("--input key cannot be empty")
        parsed[key] = value
    return parsed


def _require_input(inputs: Mapping[str, str], key: str) -> str:
    value = inputs.get(key)
    if value is None or value == "":
        raise ValueError(f"missing required --input {key}=<value>")
    return value


def _optional_path(inputs: Mapping[str, str], key: str) -> Path | None:
    value = inputs.get(key)
    return Path(value) if value else None


def _runner_workspace_init(inputs: Mapping[str, str]) -> CommandEnvelope:
    return init_workspace(Path(_require_input(inputs, "workspace_path")))


def _runner_profile_import(inputs: Mapping[str, str]) -> CommandEnvelope:
    return import_profile(
        Path(_require_input(inputs, "database_path")),
        source_path=_optional_path(inputs, "source_path"),
        source_text=inputs.get("source_text"),
        source_type=inputs.get("source_type", "yaml"),
    )


def _runner_profile_show(inputs: Mapping[str, str]) -> CommandEnvelope:
    return show_profile(
        Path(_require_input(inputs, "database_path")),
        profile_id=_require_input(inputs, "profile_id"),
    )


def _runner_job_import(inputs: Mapping[str, str]) -> CommandEnvelope:
    return import_job(
        Path(_require_input(inputs, "database_path")),
        source_path=_optional_path(inputs, "source_path"),
        source_text=inputs.get("source_text") or inputs.get("source"),
        source_type=inputs.get("source_type", "markdown"),
    )


def _runner_job_evaluate(inputs: Mapping[str, str]) -> CommandEnvelope:
    return evaluate_job(
        Path(_require_input(inputs, "database_path")),
        profile_id=_require_input(inputs, "profile_id"),
        job_id=_require_input(inputs, "job_id"),
        rubric_id=inputs.get("rubric_id"),
    )


def _runner_jobs_list(inputs: Mapping[str, str]) -> CommandEnvelope:
    return list_jobs(Path(_require_input(inputs, "database_path")))


def _runner_jobs_show(inputs: Mapping[str, str]) -> CommandEnvelope:
    return show_job(
        Path(_require_input(inputs, "database_path")),
        job_id=_require_input(inputs, "job_id"),
    )


def _runner_application_add(inputs: Mapping[str, str]) -> CommandEnvelope:
    return add_application(
        Path(_require_input(inputs, "database_path")),
        job_id=_require_input(inputs, "job_id"),
        status=inputs.get("status", "interested"),
        evaluation_id=inputs.get("evaluation_id"),
    )


def _runner_application_update(inputs: Mapping[str, str]) -> CommandEnvelope:
    return update_application(
        Path(_require_input(inputs, "database_path")),
        application_id=_require_input(inputs, "application_id"),
        status=_require_input(inputs, "status"),
        note=inputs.get("note", ""),
    )


def _runner_application_list(inputs: Mapping[str, str]) -> CommandEnvelope:
    return list_applications(Path(_require_input(inputs, "database_path")))


def _runner_application_export(inputs: Mapping[str, str]) -> CommandEnvelope:
    return export_applications(
        Path(_require_input(inputs, "database_path")),
        output_path=Path(_require_input(inputs, "output_path")),
        format=_require_input(inputs, "format"),
    )


def _runner_automation_capture_job(inputs: Mapping[str, str]) -> CommandEnvelope:
    capture = capture_text(
        source_url=_require_input(inputs, "source_url"),
        text=_require_input(inputs, "source_text"),
        captured_at=inputs.get("captured_at"),
        artifact_paths=_tuple_input(inputs.get("artifact_paths")),
    )
    return capture_job(
        Path(_require_input(inputs, "database_path")),
        capture=capture,
        source_type=inputs.get("source_type", "browser_capture"),
    )


def _runner_automation_prepare_fill_review(
    inputs: Mapping[str, str],
) -> CommandEnvelope:
    return prepare_fill_review(
        fields=_json_mapping_input(_require_input(inputs, "fields_json")),
        review_state=_require_input(inputs, "review_state"),
    )


def _tuple_input(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _json_mapping_input(value: str) -> dict[str, str]:
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("fields_json must be a JSON object")
    return {str(key): str(raw_value) for key, raw_value in parsed.items()}


def _runner_documents_suggest_tailoring(inputs: Mapping[str, str]) -> CommandEnvelope:
    return suggest_tailoring(
        Path(_require_input(inputs, "database_path")),
        profile_id=_require_input(inputs, "profile_id"),
        job_id=_require_input(inputs, "job_id"),
        evaluation_id=inputs.get("evaluation_id"),
    )


def _runner_documents_draft_cover_letter(inputs: Mapping[str, str]) -> CommandEnvelope:
    return draft_cover_letter(
        Path(_require_input(inputs, "database_path")),
        profile_id=_require_input(inputs, "profile_id"),
        job_id=_require_input(inputs, "job_id"),
        evaluation_id=inputs.get("evaluation_id"),
        requested_focus=_tuple_input(inputs.get("requested_focus")),
    )


def _runner_documents_draft_application_answer(
    inputs: Mapping[str, str],
) -> CommandEnvelope:
    return draft_application_answer(
        Path(_require_input(inputs, "database_path")),
        profile_id=_require_input(inputs, "profile_id"),
        job_id=_require_input(inputs, "job_id"),
        question=_require_input(inputs, "question"),
        evaluation_id=inputs.get("evaluation_id"),
    )


def _runner_documents_render_cover_letter(inputs: Mapping[str, str]) -> CommandEnvelope:
    return render_cover_letter(
        Path(_require_input(inputs, "database_path")),
        profile_id=_require_input(inputs, "profile_id"),
        job_id=_require_input(inputs, "job_id"),
        output_path=Path(_require_input(inputs, "output_path")),
        format=inputs.get("format", "markdown"),
        evaluation_id=inputs.get("evaluation_id"),
    )


_RUNNERS: dict[str, CommandHandler] = {
    "workspace.init": _runner_workspace_init,
    "profile.import": _runner_profile_import,
    "profile.show": _runner_profile_show,
    "jobs.import": _runner_job_import,
    "jobs.evaluate": _runner_job_evaluate,
    "jobs.list": _runner_jobs_list,
    "jobs.show": _runner_jobs_show,
    "applications.add": _runner_application_add,
    "applications.update": _runner_application_update,
    "applications.list": _runner_application_list,
    "applications.export": _runner_application_export,
    "automation.capture_job": _runner_automation_capture_job,
    "automation.prepare_fill_review": _runner_automation_prepare_fill_review,
    "documents.suggest_tailoring": _runner_documents_suggest_tailoring,
    "documents.draft_cover_letter": _runner_documents_draft_cover_letter,
    "documents.draft_application_answer": _runner_documents_draft_application_answer,
    "documents.render_cover_letter": _runner_documents_render_cover_letter,
}


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
