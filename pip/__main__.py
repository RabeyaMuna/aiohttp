import platform
import runpy
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _remove_repo_from_path(repo_root: Path) -> None:
    cwd = Path.cwd().resolve()
    sys.path = [
        path
        for path in sys.path
        if Path(path or cwd).resolve() != repo_root
    ]


def _add_pypy310_constraints(repo_root: Path) -> None:
    if (
        platform.python_implementation() != "PyPy"
        or sys.version_info >= (3, 11)
        or sys.argv[1:2] != ["install"]
    ):
        return

    constraints_file = repo_root / "requirements" / "pypy310-build-constraints.txt"
    sys.argv[2:2] = ["-c", str(constraints_file)]


def main() -> None:
    repo_root = _repo_root()
    _add_pypy310_constraints(repo_root)
    _remove_repo_from_path(repo_root)
    sys.modules.pop("pip", None)
    sys.modules.pop("pip.__main__", None)
    runpy.run_module("pip", run_name="__main__", alter_sys=True)


if __name__ == "__main__":
    main()
