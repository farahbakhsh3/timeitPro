"""
Flask dashboard for timeitPro.

Displays profiling results in separate line charts for:
- Execution Time
- CPU Usage
- Memory Usage
- Peak Memory

Features:
- Dropdown menu to select any available JSON log file
- Automatically updates charts and table based on selected log
- Charts are smaller and spaced for clarity
"""

from flask import Flask, render_template_string, request
from .utils import load_json_report, latest_log_file
from glob import glob
import os

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

    <form method="get">
        <label for="logfile">Select log file:</label>
        <select name="logfile" id="logfile" onchange="this.form.submit()">
            {% for f in logfiles %}
                <option value="{{ f }}" {% if f==selected_file %}selected{% endif %}>{{ f }}</option>
            {% endfor %}
        </select>
    </form>

    <p>Showing log file: <b>{{ selected_file }}</b></p>

    {% for metric, color in metrics %}
        <div style="margin-bottom: 30px;">
            <h3>{{ metric.replace('_',' ').title() }}</h3>
            <canvas id="{{ metric }}" width="800" height="400"></canvas>
            <script>
                const ctx_{{ metric }} = document.getElementById('{{ metric }}').getContext('2d');
                const chart_{{ metric }} = new Chart(ctx_{{ metric }}, {
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
                    options: {
                        responsive: false,
                        scales: { y: { beginAtZero: true } }
                    }
                });
            </script>
        </div>
    {% endfor %}

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
</body>
</html>
"""

def get_all_log_files():
    """Return a sorted list of all log files in the current directory."""
    return sorted([os.path.basename(f) for f in glob("timeitPro_log_*.json")])

@app.route("/", methods=["GET"])
def index():
    """Render dashboard with selected JSON log."""
    logfiles = get_all_log_files()
    if not logfiles:
        return "<h1>No log files found. Run some functions first.</h1>"

    selected_file = request.args.get("logfile") or logfiles[-1]
    reports = load_json_report(selected_file).get("runs", [])
    labels = [f"{r['function']} (Run {r['run']})" for r in reports]

    metrics = [
        ("execution_time_sec", "#3498db"),
        ("cpu_usage_percent", "#2ecc71"),
        ("memory_usage_bytes", "#e74c3c"),
        ("peak_memory_bytes", "#9b59b6")
    ]
    data = {metric: [r[metric] for r in reports] for metric, _ in metrics}

    return render_template_string(
        TEMPLATE,
        logfiles=logfiles,
        selected_file=selected_file,
        reports=reports,
        labels=labels,
        metrics=metrics,
        data=data
    )

def run_dashboard():
    """
    Run the Flask dashboard server.

    Opens a web server on localhost:5000 to display profiling results.
    """
    app.run(debug=False, port=5000)

if __name__ == "__main__":
    run_dashboard()
