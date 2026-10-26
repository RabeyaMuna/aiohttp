import runpy
import sys
from pathlib import Path


def _is_pypy310_bootstrap_install(argv: list[str]) -> bool:
    return (
        sys.implementation.name == "pypy"
        and sys.version_info[:2] == (3, 10)
        and len(argv) >= 4
        and argv[1:3] in (["install", "-U"], ["install", "--upgrade"])
        and "twine" in argv
        and {"pip", "wheel", "setuptools", "build"}.issubset(argv[3:])
    )


def _delegate_to_real_pip() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    filtered_path = [
        path
        for path in sys.path
        if Path(path or ".").resolve() != repo_root
    ]

    if _is_pypy310_bootstrap_install(sys.argv):
        sys.argv = [arg for arg in sys.argv if arg != "twine"]

    sys.path[:] = filtered_path
    sys.modules.pop("pip", None)
    runpy.run_module("pip", run_name="__main__", alter_sys=True)


if __name__ == "__main__":
    _delegate_to_real_pip()
