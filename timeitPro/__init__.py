"""
timeitPro package

Provides a powerful profiling decorator for Python functions.
Tracks execution time, CPU usage, memory usage, and peak memory.
Logs are stored in JSON files with automatic incremental filenames.
Includes a Flask-based dashboard to visualize results.

Modules:
- core.py: Contains the `timeit` decorator
- utils.py: JSON log management utilities
- dashboard.py: Flask dashboard for visualizing function profiling results
"""

from .core import timeit
from .dashboard import run_dashboard
from .utils import latest_log_file, load_json_report, save_json_report
