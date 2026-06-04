
import pytest

from res2jobworks_core.seed import seed_public_sample_workspace


def test_seed_with_private_fixture_should_report_validation_error(tmp_path) -> None:
    profile_path = tmp_path / "profile.yaml"
    job_path = tmp_path / "job.md"
    profile_path.write_text(
        "fictional fixture\nname: Example\napi_key: secret\n",
        encoding="utf-8",
    )
    job_path.write_text("# fictional fixture job\n", encoding="utf-8")

    with pytest.raises(ValueError, match="not public-generic"):
        seed_public_sample_workspace(
            tmp_path / "workspace.sqlite3",
            profile_path=profile_path,
            job_path=job_path,
        )
