"""
Integration tests for the Flask dashboard of timeitPro.

Ensures that endpoints return expected responses and valid HTML.
"""

from __future__ import annotations
import json
from pathlib import Path
import pytest
from timeitPro.dashboard import app as flask_app  # existing app instance


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """
    Fixture to create a Flask test client with temporary log directory.
    """
    # Create a temporary log directory
    log_dir: Path = tmp_path / "logs"
    log_dir.mkdir()

    # Create a fake log file
    sample_log: dict = {
        "runs": [
            {
                "function": "dummy_func",
                "run": 1,
                "execution_time_sec": 0.1,
                "cpu_usage_percent": 5.0,
                "memory_usage_bytes": 10000,
                "peak_memory_bytes": 15000
            },
            {
                "function": "dummy_func",
                "run": 2,
                "execution_time_sec": 0.11,
                "cpu_usage_percent": 6.0,
                "memory_usage_bytes": 11000,
                "peak_memory_bytes": 16000
            }
        ],
        "averages": {
            "average_execution_time_sec": 0.105,
            "average_cpu_usage_percent": 5.5,
            "average_memory_usage_bytes": 10500,
            "average_peak_memory_bytes": 15500
        }
    }

    file_path: Path = log_dir / "timeitPro_log_000001.json"
    file_path.write_text(json.dumps(sample_log))

    # Override log directory in utils
    from timeitPro import utils
    monkeypatch.setattr(utils, "LOG_DIR", str(log_dir))

    flask_app.testing = True
    return flask_app.test_client()


def test_index_no_logs(monkeypatch: pytest.MonkeyPatch):
    """
    Test index page when no logs exist.
    """
    from timeitPro import utils
    monkeypatch.setattr(utils, "LOG_DIR", "/non/existent/path")
    flask_app.testing = True
    client = flask_app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"No log files found" in response.data


def test_index_with_logs_all_view(client):
    """
    Test index page with logs and view=all.
    """
    response = client.get("/")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "timeitPro_log_000001.json" in html
    assert "Detailed Runs" in html
    assert "Execution Time" in html
    assert "CPU %" in html


def test_index_with_logs_average_view(client):
    """
    Test index page with logs and view=average.
    """
    response = client.get("/?view=average")
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Average Metrics" in html
    assert "Average Execution Time" in html
    assert "Average CPU Usage" in html
    assert "Average Memory Usage" in html
    assert "Average Peak Memory" in html
