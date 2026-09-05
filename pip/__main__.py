"""Shim to fix PyPy 3.10 bootstrap pip shadowing issue.

When running on PyPy 3.10, the repository root is on sys.path, which causes
the local pip/ package to shadow the real pip module from site-packages.
This shim detects the PyPy 3.10 bootstrap scenario and delegates to the
real pip module after cleaning up sys.path and sys.modules.
"""
import sys
import os
import runpy


def is_pypy_310_bootstrap():
    """Check if we're running on PyPy 3.10 in bootstrap install mode."""
    if not hasattr(sys, 'pypy_version_info'):
        return False
    # Check for PyPy 3.10.x
    version_info = sys.version_info
    return version_info.major == 3 and version_info.minor == 10


def fix_pypy_310_pip_shadowing():
    """Fix pip shadowing on PyPy 3.10 bootstrap installs."""
    # Get the repository root (parent of pip/ directory)
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Filter out the repo root from sys.path
    original_path = sys.path[:]
    sys.path[:] = [p for p in sys.path if os.path.abspath(p) != repo_root]
    
    # Remove any preloaded pip from sys.modules
    modules_to_remove = [key for key in sys.modules if key == 'pip' or key.startswith('pip.')]
    for mod in modules_to_remove:
        del sys.modules[mod]
    
    # Remove 'twine' from sys.argv if present (not needed for bootstrap)
    if 'twine' in sys.argv:
        sys.argv = [arg for arg in sys.argv if arg != 'twine']


def main():
    """Main entry point for the pip shim."""
    if is_pypy_310_bootstrap():
        fix_pypy_310_pip_shadowing()
    
    # Delegate to the real pip module
    runpy.run_module('pip', run_name='__main__', alter_sys=True)


if __name__ == '__main__':
    main()
