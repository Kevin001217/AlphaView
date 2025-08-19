from flask import Flask, render_template_string
from portfolio.scripts import calculate_percentages, calculate_pnl

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="60">
    <title>Portfolio Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 24px; background: #0b0f14; color: #e6edf3; }
        h1 { margin-bottom: 12px; }
        table { border-collapse: collapse; width: 100%; margin-top: 12px; }
        th, td { border-bottom: 1px solid #1f2732; padding: 8px 10px; text-align: right; }
        th:first-child, td:first-child { text-align: left; }
        tr:hover { background: #111826; }
    </style>
</head>
<body>
    <h1>Portfolio Report <small>(auto-refresh 60s)</small></h1>
    <div><strong>Total (incl. cash):</strong> ${{ "{:.2f}".format(total) }}</div>
    <table>
        <thead>
            <tr>
                <th>Ticker</th><th>Shares</th><th>Price</th>
                <th>Avg Cost</th><th>Value</th><th>PnL</th><th>PnL %</th><th>Weight</th>
            </tr>
        </thead>
        <tbody>
            {% for r in rows %}
            <tr>
                <td>{{ r['Ticker'] }}</td>
                <td>{{ "{:.2f}".format(r['Shares']) }}</td>
                <td>{{ "{:.2f}".format(r['Price']) }}</td>
                <td>{{ "{:.2f}".format(r['AvgCost']) }}</td>
                <td>{{ "{:.2f}".format(r['Value']) }}</td>
                <td>{{ "{:.2f}".format(r['PnL']) }}</td>
                <td>{{ "{:.2f}".format(r['PnL_%']) }}%</td>
                <td>{{ pct[r['Ticker']] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route("/")
def portfolio_page():
    total, pct = calculate_percentages.get_percentages()
    rows, totals = calculate_pnl.get_pnl()
    return render_template_string(HTML_TEMPLATE, total=total, pct=pct, rows=rows, totals=totals)

if __name__ == "__main__":
    app.run(debug=True)
