"""
Utility functions for timeitPro.

Handles JSON log management, incremental filenames, and loading logs for dashboard.
"""

import json
import os
from glob import glob
from typing import Any, Optional

# === Configuration ===
LOG_DIR = "."
LOG_PREFIX = "timeitPro_log_"
LOG_EXT = ".json"


# === Internal Helpers ===

def _log_pattern() -> str:
    """Return the glob pattern for locating log files."""
    return os.path.join(LOG_DIR, f"{LOG_PREFIX}*{LOG_EXT}")


def _extract_counter(filename: str) -> Optional[int]:
    """
    Extract numeric counter from filename.

    Args:
        filename: Full or base name of a log file.

    Returns:
        int | None: The numeric counter, or None if invalid.
    """
    name = os.path.basename(filename)
    if not (name.startswith(LOG_PREFIX) and name.endswith(LOG_EXT)):
        return None

    num_part = name[len(LOG_PREFIX):-len(LOG_EXT)]
    return int(num_part) if num_part.isdigit() else None


# === Core Functions ===

def _next_log_filename() -> str:
    """
    Generate the next available log filename with zero-padded counter.

    Returns:
        str: Full path of the next log file to create.
    """
    counters = [
        n for n in (_extract_counter(f) for f in glob(_log_pattern())) if n is not None
    ]
    next_counter = (max(counters) + 1) if counters else 1
    return os.path.join(LOG_DIR, f"{LOG_PREFIX}{next_counter:06d}{LOG_EXT}")


def save_json_report(data: dict[str, Any]) -> str:
    """
    Save profiling data to a new JSON file with incremental counter.

    Args:
        data (dict): Dictionary containing profiling data.

    Returns:
        str: The filename of the created JSON log.
    """
    filename = _next_log_filename()
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename


def load_json_report(filename: str) -> dict[str, Any]:
    """
    Load a JSON log file.

    Args:
        filename (str): Path to JSON log file.

    Returns:
        dict: Dictionary containing profiling data.
    """
    if not os.path.isfile(filename):
        return {"runs": []}
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def latest_log_file() -> Optional[str]:
    """
    Get the most recent log file based on numeric counter in filename.

    Returns:
        str | None: Path to the latest log file, or None if no valid logs exist.
    """
    files = glob(_log_pattern())
    if not files:
        return None

    valid_files = [(f, _extract_counter(f)) for f in files]
    valid_files = [(f, n) for f, n in valid_files if n is not None]

    if not valid_files:
        return None

    latest_file, _ = max(valid_files, key=lambda x: x[1])
    return latest_file


def get_all_log_files() -> list[str]:
    """
    Return a sorted list of all log files (by numeric order).
    """
    files = [
        (os.path.basename(f), _extract_counter(f))
        for f in glob(_log_pattern())
    ]
    files = [(name, n) for name, n in files if n is not None]
    return [name for name, _ in sorted(files, key=lambda x: x[1])]
