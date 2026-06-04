#!/usr/bin/env python
"""Source-tree script for generating registry-backed agent wrappers."""

import sys
from pathlib import Path


def _add_source_paths() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    for source_path in [
        repo_root / "packages" / "skills" / "src",
        repo_root / "packages" / "core" / "src",
    ]:
        if source_path.exists() and str(source_path) not in sys.path:
            sys.path.insert(0, str(source_path))


_add_source_paths()

from res2jobworks_skills.generator import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
