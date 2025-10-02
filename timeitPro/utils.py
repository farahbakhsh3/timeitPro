"""
Utility functions for timeitPro.

Handles JSON log management, incremental filenames, and loading logs for dashboard.
"""

import json
import os
from glob import glob

LOG_DIR = "."
LOG_PREFIX = "timeitPro_log_"
LOG_EXT = ".json"

def _next_log_filename():
    """
    Generate the next available log filename with zero-padded counter.

    Returns:
        str: Full path of the next log file to create
    """
    existing = sorted(glob(os.path.join(LOG_DIR, LOG_PREFIX + "*.json")))
    if not existing:
        counter = 1
    else:
        last_file = os.path.basename(existing[-1])
        try:
            last_counter = int(last_file[len(LOG_PREFIX):-len(LOG_EXT)])
            counter = last_counter + 1
        except ValueError:
            counter = len(existing) + 1
    return os.path.join(LOG_DIR, f"{LOG_PREFIX}{counter:06d}{LOG_EXT}")

def save_json_report(data: dict) -> str:
    """
    Save profiling data to a new JSON file with incremental counter.

    Args:
        data (dict): Dictionary containing profiling data.

    Returns:
        str: The filename of the created JSON log.
    """
    filename = _next_log_filename()
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return filename

def load_json_report(filename: str) -> dict:
    """
    Load JSON log file.

    Args:
        filename (str): Path to JSON log file.

    Returns:
        dict: Dictionary containing profiling data.
    """
    if not os.path.exists(filename):
        return {"runs": []}
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def latest_log_file() -> str:
    """
    Get the most recent log file.

    Returns:
        str: Path to the latest log file or None if no logs exist.
    """
    existing = sorted(glob(os.path.join(LOG_DIR, LOG_PREFIX + "*.json")))
    if not existing:
        return None
    return existing[-1]
