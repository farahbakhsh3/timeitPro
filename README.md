# timeitPro

**timeitPro** is an advanced Python function profiler with JSON logging and a Flask dashboard.

## Features

- Decorator `@timeit(runs=N, show_console=True)` to profile functions.
- Measures:
  - Execution time
  - CPU usage (%)
  - Memory usage (bytes)
  - Peak memory (bytes)
- Each run generates a **new JSON log** with incremental filename.
- Flask dashboard:
  - Displays results as **separate line charts** for each metric.
  - Dropdown to select which log file to display.
  - Table with detailed run information.
- Console output optional (`show_console=True/False`).

## Installation

```bash
pip install -r requirements.txt
```

Dependencies:
- Flask
- psutil

## Usage

```python
from timeitPro import timeit, run_dashboard

# Profile a function with 3 runs and console output
@timeit(runs=3, show_console=True)
def my_func():
    total = sum(range(1000000))
    return total

my_func()

# Run the dashboard
run_dashboard()
```

## JSON Logs

- Logs are saved as `timeitPro_log_000001.json`, `timeitPro_log_000002.json`, ...
- Each JSON contains all runs from a profiling session.
- Dashboard automatically lists all available log files.

## Dashboard

- Access via: `http://localhost:5000/`
- Features:
  - Dropdown to select log file
  - Separate line charts for execution time, CPU, memory, peak memory
  - Table of detailed runs

## License

MIT License
