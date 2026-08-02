"""Test bootstrap shim for GitHub Actions.

This package is intentionally not part of aiohttp's packaged modules. It exists
only so ``python -m pip`` from the repository root can avoid installing
unnecessary publishing dependencies on unsupported PyPy bootstrap jobs.
"""

