"""Delegate to real pip, with PyPy 3.10 CI bootstrap constraints."""

from __future__ import annotations

import os
import platform
import runpy
import sys
from pathlib import Path


def _needs_ci_bootstrap_constraints() -> bool:
    args = sys.argv[1:]
    return (
        os.environ.get("GITHUB_ACTIONS") == "true"
        and platform.python_implementation() == "PyPy"
        and sys.version_info < (3, 11)
        and "install" in args
        and "twine" in args
    )


def _drop_repo_from_import_path(repo_root: Path) -> None:
    cwd = Path.cwd().resolve()
    filtered_path: list[str] = []
    for entry in sys.path:
        entry_path = cwd if entry == "" else Path(entry).resolve()
        if entry_path != repo_root:
            filtered_path.append(entry)
    sys.path[:] = filtered_path


repo_root = Path(__file__).resolve().parents[1]

if _needs_ci_bootstrap_constraints():
    constraints = repo_root / "requirements" / "ci-bootstrap-constraints.txt"
    os.environ.setdefault("PIP_CONSTRAINT", str(constraints))

_drop_repo_from_import_path(repo_root)
sys.modules.pop("pip", None)
sys.modules.pop("pip.__main__", None)
runpy.run_module("pip", run_name="__main__", alter_sys=True)
