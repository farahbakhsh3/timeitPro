"""
Unit tests for utils.py in timeitPro package.
Covers JSON log management, incremental filenames, and loading logs.
"""

from __future__ import annotations
import json
from pathlib import Path
import pytest
import os
from timeitPro import utils


def test_extract_counter_valid() -> None:
    """Test extracting numeric counter from valid filenames."""
    assert utils._extract_counter("timeitPro_log_000001.json") == 1
    assert utils._extract_counter("timeitPro_log_123456.json") == 123456


def test_extract_counter_invalid() -> None:
    """Test extracting counter from invalid filenames."""
    assert utils._extract_counter("otherfile.json") is None
    assert utils._extract_counter("timeitPro_log_xyz.json") is None


def test_next_log_filename(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test generating the next incremental log filename."""
    monkeypatch.setattr(utils, "LOG_DIR", str(tmp_path))

    # No existing files => counter should start at 1
    next_file = utils._next_log_filename()
    assert next_file.endswith("timeitPro_log_000001.json")

    # Create dummy log file to simulate existing log
    dummy_file = tmp_path / "timeitPro_log_000001.json"
    dummy_file.write_text("{}")

    # Next filename should increment
    next_file2 = utils._next_log_filename()
    assert next_file2.endswith("timeitPro_log_000002.json")


def test_save_and_load_json_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test saving and loading JSON reports."""
    monkeypatch.setattr(utils, "LOG_DIR", str(tmp_path))

    data = {"runs": [{"time": 0.1}]}
    filename = utils.save_json_report(data)
    assert Path(filename).exists()

    loaded = utils.load_json_report(filename)
    assert loaded == data

    # Loading non-existent file returns default structure
    non_exist = tmp_path / "nonexistent.json"
    assert utils.load_json_report(str(non_exist)) == {"runs": []}


def test_latest_log_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test retrieving the most recent log file."""
    monkeypatch.setattr(utils, "LOG_DIR", str(tmp_path))

    # No logs => None
    assert utils.latest_log_file() is None

    # Create some log files
    files = [
        tmp_path / f"timeitPro_log_{i:06d}.json" for i in [1, 3, 2]
    ]
    for f in files:
        f.write_text("{}")

    latest = utils.latest_log_file()
    assert latest.endswith("timeitPro_log_000003.json")


def test_get_all_log_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test retrieving all log files in numeric order."""
    monkeypatch.setattr(utils, "LOG_DIR", str(tmp_path))

    files = [
        tmp_path / f"timeitPro_log_{i:06d}.json" for i in [5, 1, 3]
    ]
    for f in files:
        f.write_text("{}")

    all_files = utils.get_all_log_files()
    assert all_files == ["timeitPro_log_000001.json", "timeitPro_log_000003.json", "timeitPro_log_000005.json"]

def test_latest_log_file_none(tmp_path: Path, monkeypatch: "MonkeyPatch") -> None:
    """
    Test `latest_log_file` returns None when no valid log files exist.

    Scenarios covered:
    1. The log directory is empty.
    2. The directory contains only invalid files.
    """
    # Empty log directory
    monkeypatch.setattr("timeitPro.utils.LOG_DIR", tmp_path)
    assert utils.latest_log_file() is None

    # Directory contains an invalid file
    invalid_file = tmp_path / "timeitPro_log_a.json"
    invalid_file.write_text("dummy content")
    assert utils.latest_log_file() is None
