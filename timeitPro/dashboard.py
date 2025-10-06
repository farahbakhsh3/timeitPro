"""
Flask dashboard for timeitPro.

Displays profiling results in separate charts for:
- Execution Time
- CPU Usage
- Memory Usage
- Peak Memory

Features:
- Dropdown to select JSON log file
- Toggle to display "All runs" or "Averages only"
- Separate charts for per-run and average metrics
- Automatically updates charts and table based on selection
"""

from flask import Flask, render_template_string, request
from typing import List, Dict, Any, Tuple
from .utils import load_json_report, get_all_log_files

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>timeitPro Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body style="font-family: Arial, sans-serif; margin: 40px;">
    <h1>timeitPro Report</h1>

    <!-- Form to select log file and view type -->
    <form method="get">
        <label for="logfile">Select log file:</label>
        <select name="logfile" id="logfile" onchange="this.form.submit()">
            {% for f in logfiles %}
                <option value="{{ f }}" {% if f==selected_file %}selected{% endif %}>{{ f }}</option>
            {% endfor %}
        </select>

        <label style="margin-left:20px;">Display:</label>
        <select name="view" onchange="this.form.submit()">
            <option value="all" {% if view=='all' %}selected{% endif %}>All Runs</option>
            <option value="average" {% if view=='average' %}selected{% endif %}>Averages Only</option>
        </select>
    </form>

    <p>Showing log file: <b>{{ selected_file }}</b></p>

    {% if view == 'average' and averages %}
        <!-- Averages section -->
        <h2>Average Metrics</h2>
        <ul>
            <li>Average Execution Time: {{ averages.average_execution_time_sec }} s</li>
            <li>Average CPU Usage: {{ averages.average_cpu_usage_percent }} %</li>
            <li>Average Memory Usage: {{ averages.average_memory_usage_bytes }} bytes</li>
            <li>Average Peak Memory: {{ averages.average_peak_memory_bytes }} bytes</li>
        </ul>

        {% for metric, color in metrics %}
            <div style="margin-bottom: 30px;">
                <h3>{{ metric.replace('_',' ').title() }} (Average)</h3>
                <canvas id="{{ metric }}_avg" width="800" height="400"></canvas>
                <script>
                    const ctx_{{ metric }}_avg = document.getElementById('{{ metric }}_avg').getContext('2d');
                    new Chart(ctx_{{ metric }}_avg, {
                        type: 'bar',
                        data: {
                            labels: ['Average'],
                            datasets: [{
                                label: '{{ metric.replace("_"," ").title() }}',
                                data: [{{ averages[metric] }}],
                                backgroundColor: '{{ color }}'
                            }]
                        },
                        options: { responsive: false, scales: { y: { beginAtZero: true } } }
                    });
                </script>
            </div>
        {% endfor %}

    {% else %}
        <!-- All runs section -->
        {% for metric, color in metrics %}
            <div style="margin-bottom: 30px;">
                <h3>{{ metric.replace('_',' ').title() }} (All Runs)</h3>
                <canvas id="{{ metric }}" width="800" height="400"></canvas>
                <script>
                    const ctx_{{ metric }} = document.getElementById('{{ metric }}').getContext('2d');
                    new Chart(ctx_{{ metric }}, {
                        type: 'line',
                        data: {
                            labels: {{ labels|tojson }},
                            datasets: [{
                                label: '{{ metric.replace("_"," ").title() }}',
                                data: {{ data[metric]|tojson }},
                                borderColor: '{{ color }}',
                                fill: false,
                                tension: 0.1
                            }]
                        },
                        options: { responsive: false, scales: { y: { beginAtZero: true } } }
                    });
                </script>
            </div>
        {% endfor %}

        <!-- Detailed table for all runs -->
        <h2>Detailed Runs</h2>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>Function</th><th>Run</th><th>Execution Time (s)</th>
                <th>CPU %</th><th>Memory (bytes)</th><th>Peak Memory</th>
            </tr>
            {% for r in reports %}
            <tr>
                <td>{{ r.function }}</td><td>{{ r.run }}</td><td>{{ r.execution_time_sec }}</td>
                <td>{{ r.cpu_usage_percent }}</td><td>{{ r.memory_usage_bytes }}</td><td>{{ r.peak_memory_bytes }}</td>
            </tr>
            {% endfor %}
        </table>
    {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index() -> str:
    """
    Render the dashboard page.

    Retrieves the selected log file and displays either all runs or averages only.
    """
    logfiles: List[str] = get_all_log_files()
    if not logfiles:
        return "<h1>No log files found. Run some functions first.</h1>"

    selected_file: str = request.args.get("logfile") or logfiles[-1]
    view: str = request.args.get("view", "all")  # 'all' or 'average'

    report_data: Dict[str, Any] = load_json_report(selected_file)
    reports: List[Dict[str, Any]] = report_data.get("runs", [])
    averages: Dict[str, Any] = report_data.get("averages", {})

    labels: List[str] = [f"{r['function']} (Run {r['run']})" for r in reports]

    metrics: List[Tuple[str, str]] = [
        ("execution_time_sec", "#3498db"),
        ("cpu_usage_percent", "#2ecc71"),
        ("memory_usage_bytes", "#e74c3c"),
        ("peak_memory_bytes", "#9b59b6")
    ]

    data: Dict[str, List[Any]] = {
        metric: [r[metric] for r in reports] for metric, _ in metrics
    }

    return render_template_string(
        TEMPLATE,
        logfiles=logfiles,
        selected_file=selected_file,
        reports=reports,
        labels=labels,
        metrics=metrics,
        data=data,
        averages=averages,
        view=view
    )


def run_dashboard() -> None:
    """
    Run the Flask dashboard server.

    Opens a web server on localhost:5000 to display profiling results.
    """
    app.run(debug=False, port=5000)


if __name__ == "__main__":
    run_dashboard()
