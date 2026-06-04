"""Test path setup for the source-tree skills package."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_SRC = REPO_ROOT / "packages" / "skills" / "src"

if str(SKILLS_SRC) not in sys.path:
    sys.path.insert(0, str(SKILLS_SRC))
