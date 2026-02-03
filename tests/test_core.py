"""
Unit tests for core.py in timeitPro package.
Covers the `timeit` decorator functionality, multiple runs, and JSON log saving.
"""

from __future__ import annotations
from pathlib import Path
import pytest
from typing import Any, Callable
from timeitPro import core, utils


def test_timeit_returns_correct_value(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test that the `timeit` decorator returns the original function's result.
    """
    monkeypatch.setattr(utils, "LOG_DIR", str(tmp_path))

    @core.timeit(runs=2, show_console=False)
    def add(a: int, b: int) -> int:
        """Simple addition function."""
        return a + b

    result = add(3, 5)
    assert result == 8


def test_timeit_executes_correct_number_of_runs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test that the decorator executes the function the specified number of times.
    """
    monkeypatch.setattr(utils, "LOG_DIR", str(tmp_path))
    call_count = {"count": 0}

    @core.timeit(runs=5, show_console=False)
    def dummy() -> None:
        call_count["count"] += 1

    dummy()
    assert call_count["count"] == 5


def test_timeit_creates_json_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test that the decorator generates a valid JSON log file.
    """
    monkeypatch.setattr(utils, "LOG_DIR", str(tmp_path))

    @core.timeit(runs=3, show_console=False)
    def dummy_func() -> int:
        return 42

    dummy_func()

    log_files = list(tmp_path.glob("timeitPro_log_*.json"))
    assert len(log_files) == 1

    # Validate content
    import json
    content: dict = json.loads(log_files[0].read_text())
    assert content["function"] == "dummy_func"
    assert content["total_runs"] == 3
    assert len(content["runs"]) == 3
    assert "execution_time_sec" in content["runs"][0]
    assert "cpu_usage_percent" in content["runs"][0]
    assert "memory_usage_bytes" in content["runs"][0]
    assert "peak_memory_bytes" in content["runs"][0]
    assert "averages" in content


def test_timeit_with_show_average(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: Any) -> None:
    """
    Test console output including averages when show_average is True.
    """
    monkeypatch.setattr(utils, "LOG_DIR", str(tmp_path))

    @core.timeit(runs=2, show_console=True, show_average=True)
    def dummy_func() -> int:
        return 1

    dummy_func()
    captured = capsys.readouterr()
    # Check that average results appear in output
    assert "Average Results" in captured.out
    assert "dummy_func" in captured.out
    assert "Saved log to:" in captured.out


def test_timeit_runs_must_be_positive() -> None:
    """Test that runs must be >= 1."""
    with pytest.raises(ValueError):
        core.timeit(runs=0)
