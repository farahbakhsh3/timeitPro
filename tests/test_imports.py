"""
Basic import and structure validation tests for timeitPro.
Ensures that all major modules import successfully.
"""

from __future__ import annotations


def test_import_core() -> None:
    """Test that the core module imports without errors."""
    import timeitPro.core  # noqa: F401


def test_import_dashboard() -> None:
    """Test that the dashboard module imports without errors."""
    import timeitPro.dashboard  # noqa: F401


def test_package_has_version() -> None:
    """Ensure that __version__ attribute exists."""
    import timeitPro
    assert hasattr(timeitPro, "__version__")
