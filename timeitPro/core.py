"""
Core module for timeitPro.

Provides the `timeit` decorator which profiles functions over multiple runs.
Each run measures execution time, CPU usage, memory usage, and peak memory.
All runs are saved into a new JSON log file with an incremental filename.

Decorator Arguments:
- runs (int): Number of repetitions for the function
- show_console (bool): Whether to print each run's results to the console
"""

import time
import psutil
import tracemalloc
from functools import wraps
from .utils import save_json_report

def timeit(runs: int = 1, show_console: bool = True):
    """
    Profile a function over multiple runs and save results to JSON logs.

    Args:
        runs (int): Number of times to execute the function.
        show_console (bool): If True, prints results of each run to console.

    Returns:
        The original function's return value (from last run).

    Side Effects:
        - Creates a new JSON log file for the runs (incremental filename)
        - Optionally prints each run's statistics to console
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logs = []

            for run_idx in range(1, runs + 1):
                process = psutil.Process()
                tracemalloc.start()
                start_time = time.perf_counter()
                start_mem = process.memory_info().rss
                start_cpu = process.cpu_percent(interval=None)

                result = func(*args, **kwargs)

                end_time = time.perf_counter()
                end_mem = process.memory_info().rss
                end_cpu = process.cpu_percent(interval=None)
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                report = {
                    "function": func.__name__,
                    "run": run_idx,
                    "execution_time_sec": round(end_time - start_time, 6),
                    "cpu_usage_percent": end_cpu,
                    "memory_usage_bytes": end_mem - start_mem,
                    "peak_memory_bytes": peak,
                }

                logs.append(report)

                if show_console:
                    print(f"[Run {run_idx}/{runs}] {func.__name__}: "
                          f"Time={report['execution_time_sec']}s, "
                          f"CPU={report['cpu_usage_percent']}%, "
                          f"Memory={report['memory_usage_bytes']} bytes, "
                          f"Peak={report['peak_memory_bytes']} bytes")

            filename = save_json_report({"runs": logs})
            if show_console:
                print(f"Saved log to: {filename}")

            return result
        return wrapper
    return decorator
