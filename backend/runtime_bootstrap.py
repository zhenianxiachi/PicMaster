from __future__ import annotations

import os
import sys
from pathlib import Path


def prefer_repo_python() -> None:
    """Re-exec the current command with the repo virtualenv when available."""
    if os.environ.get("PICMASTER_BOOTSTRAPPED") == "1":
        return

    root_dir = Path(__file__).resolve().parents[1]
    current_python = Path(sys.executable).resolve()
    candidates = (
        root_dir / ".venv" / "Scripts" / "python.exe",
        root_dir / ".venv" / "bin" / "python",
    )

    for candidate in candidates:
        if not candidate.exists():
            continue

        repo_python = candidate.resolve()
        if repo_python == current_python:
            return

        env = os.environ.copy()
        env["PICMASTER_BOOTSTRAPPED"] = "1"
        os.execve(str(repo_python), [str(repo_python), *sys.argv], env)
