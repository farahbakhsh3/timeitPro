"""
Core module for timeitPro.

Provides a `timeit` decorator to profile functions over multiple runs.
Each run records execution time, CPU usage, memory usage, and peak memory.
All runs, along with averages, are saved to a JSON log file with an incremental filename.

Decorator Arguments:
- runs (int): Number of repetitions of the function.
- show_console (bool): Whether to print per-run results.
- show_average (bool): Whether to print average metrics at the end.
"""

import time
import psutil
import tracemalloc
from functools import wraps
from typing import Any, Callable, Dict, List
from .utils import save_json_report


def timeit(
    runs: int = 1,
    show_console: bool = True,
    show_average: bool = True
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to profile a function over multiple executions.

    Measures execution time, CPU usage, memory usage, and peak memory.
    Saves all runs and averages to a JSON log file.

    Args:
        runs (int): Number of times to execute the function.
        show_console (bool): If True, prints stats for each run.
        show_average (bool): If True, prints average metrics after all runs.

    Returns:
        Callable: Wrapped function returning the last run's result.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper that profiles the function."""
            logs: List[Dict[str, Any]] = []
            result: Any = None

            # Run the function multiple times
            for run_idx in range(1, runs + 1):
                process: psutil.Process = psutil.Process()
                tracemalloc.start()

                # Start metrics
                start_time: float = time.perf_counter()
                start_mem: int = process.memory_info().rss
                start_cpu: float = process.cpu_percent(interval=None)

                # Execute original function
                result = func(*args, **kwargs)

                # End metrics
                end_time: float = time.perf_counter()
                end_mem: int = process.memory_info().rss
                end_cpu: float = process.cpu_percent(interval=None)
                _, peak_mem: int = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                # Per-run report
                report: Dict[str, Any] = {
                    "function": func.__name__,
                    "run": run_idx,
                    "execution_time_sec": round(end_time - start_time, 6),
                    "cpu_usage_percent": round(end_cpu, 2),
                    "memory_usage_bytes": end_mem - start_mem,
                    "peak_memory_bytes": peak_mem,
                }

                logs.append(report)

                # Optional per-run console output
                if show_console:
                    print(
                        f"[Run {run_idx}/{runs}] {func.__name__}: "
                        f"Time={report['execution_time_sec']}s, "
                        f"CPU={report['cpu_usage_percent']}%, "
                        f"Memory={report['memory_usage_bytes']} bytes, "
                        f"Peak={report['peak_memory_bytes']} bytes"
                    )

            # -----------------------------
            # Compute averages
            # -----------------------------
            averages: Dict[str, Any] = {
                "average_execution_time_sec": round(
                    sum(r["execution_time_sec"] for r in logs) / runs, 6
                ),
                "average_cpu_usage_percent": round(
                    sum(r["cpu_usage_percent"] for r in logs) / runs, 2
                ),
                "average_memory_usage_bytes": int(
                    sum(r["memory_usage_bytes"] for r in logs) / runs
                ),
                "average_peak_memory_bytes": int(
                    sum(r["peak_memory_bytes"] for r in logs) / runs
                ),
            }

            # -----------------------------
            # Optional average console output
            # -----------------------------
            if show_console and show_average:
                print("\n  Average Results")
                print(f"   Function: {func.__name__}")
                print(f"   Runs: {runs}")
                print(f"   Avg Time: {averages['average_execution_time_sec']} s")
                print(f"   Avg CPU: {averages['average_cpu_usage_percent']} %")
                print(f"   Avg Memory: {averages['average_memory_usage_bytes']} bytes")
                print(f"   Avg Peak Memory: {averages['average_peak_memory_bytes']} bytes\n")

            # -----------------------------
            # Save results to JSON log
            # -----------------------------
            full_log: Dict[str, Any] = {
                "function": func.__name__,
                "total_runs": runs,
                "runs": logs,
                "averages": averages,
            }

            filename: str = save_json_report(full_log)

            # -----------------------------
            # Show log saved message after averages
            # -----------------------------
            if show_console:
                print(f"Saved log to: {filename}")

            return result

        return wrapper

    return decorator
