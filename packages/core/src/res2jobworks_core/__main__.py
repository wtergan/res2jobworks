"""Smoke-check entrypoint for the core package."""

from res2jobworks_core.config import Res2JobWorksConfig


def main() -> None:
    """Print a tiny package health signal for bootstrap verification."""
    config = Res2JobWorksConfig()
    print(f"res2jobworks-core ok workspace={config.workspace_dir}")


if __name__ == "__main__":
    main()

