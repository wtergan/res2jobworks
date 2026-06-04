"""Read-only command workflows for profile, job, and detail views."""

from pathlib import Path

from res2jobworks_core.commands._support import failure
from res2jobworks_core.contracts import CommandEnvelope
from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def show_profile(database_path: Path | str, *, profile_id: str) -> CommandEnvelope:
    """Return one stored profile summary through a command envelope."""
    command = "profile.show"
    inputs = {"database_path": str(database_path), "profile_id": profile_id}
    try:
        repository = SQLiteRepository(database_path)
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={
                "profile": repository.get_profile(profile_id),
                "resume_sources": repository.list_resume_sources(profile_id),
            },
        )
    except RepositoryError as exc:
        return failure(command, inputs, exc)


def list_jobs(database_path: Path | str) -> CommandEnvelope:
    """Return stored jobs with application and evaluation summary fields."""
    command = "jobs.list"
    inputs = {"database_path": str(database_path)}
    try:
        repository = SQLiteRepository(database_path)
        applications = repository.list_applications()
        evaluations = repository.list_evaluations()
        jobs = []
        for job in repository.list_jobs():
            job_applications = [
                application
                for application in applications
                if application["job_id"] == job["id"]
            ]
            job_evaluations = [
                evaluation
                for evaluation in evaluations
                if evaluation["job_id"] == job["id"]
            ]
            jobs.append(
                {
                    **job,
                    "application_count": len(job_applications),
                    "current_status": (
                        job_applications[-1]["current_status"]
                        if job_applications
                        else None
                    ),
                    "latest_score": (
                        job_evaluations[-1]["score"] if job_evaluations else None
                    ),
                }
            )
        return CommandEnvelope.success(command, inputs=inputs, data={"jobs": jobs})
    except RepositoryError as exc:
        return failure(command, inputs, exc)


def show_job(database_path: Path | str, *, job_id: str) -> CommandEnvelope:
    """Return one stored job with sources, evaluations, and applications."""
    command = "jobs.show"
    inputs = {"database_path": str(database_path), "job_id": job_id}
    try:
        repository = SQLiteRepository(database_path)
        evaluations = [
            repository.get_evaluation(evaluation["id"])
            for evaluation in repository.list_evaluations()
            if evaluation["job_id"] == job_id
        ]
        applications = [
            application
            for application in repository.list_applications()
            if application["job_id"] == job_id
        ]
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={
                "job": repository.get_job(job_id),
                "job_sources": repository.list_job_sources(job_id),
                "evaluations": evaluations,
                "applications": applications,
            },
        )
    except RepositoryError as exc:
        return failure(command, inputs, exc)
