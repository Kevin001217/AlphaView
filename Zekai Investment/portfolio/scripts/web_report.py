# portfolio/scripts/web_report.py
from pathlib import Path
from portfolio.scripts import calculate_percentages, calculate_pnl

HTML_PATH = Path(__file__).resolve().parents[1] / "data" / "portfolio_report.html"

def build_html():
    total, pct = calculate_percentages.get_percentages()
    rows, totals = calculate_pnl.get_pnl()

    def fmt(n, width=0, decimals=2):
        return "" if n is None else f"{n:.{decimals}f}"

    # simple CSS + auto-refresh every 60s 
    html = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'>",
        "<meta http-equiv='refresh' content='60'>",
        "<title>Portfolio Report</title>",
        "<style>",
        "body{font-family:ui-sans-serif,system-ui,Arial;margin:24px;background:#0b0f14;color:#e6edf3}",
        "h1{margin:0 0 12px 0;font-size:22px}",
        "small{color:#9aa4af}",
        "table{border-collapse:collapse;width:100%;margin-top:12px}",
        "th,td{border-bottom:1px solid #1f2732;padding:8px 10px;text-align:right}",
        "th:first-child,td:first-child{text-align:left}",
        "tr:hover{background:#111826}",
        ".totals{margin-top:16px;display:grid;grid-template-columns:200px 1fr;gap:6px 16px;max-width:420px}",
        ".label{color:#9aa4af}",
        "</style></head><body>",
        "<h1>Portfolio Report </h1>",
        f"<div><strong>Total (incl. cash):</strong> ${fmt(total)}</div>",
        "<table><thead><tr>",
        "<th>Ticker</th><th>Shares</th><th>Price</th><th>Avg Cost</th><th>Value</th><th>PnL</th><th>PnL %</th><th>Weight</th>",
        "</tr></thead><tbody>"
    ]

    for r in rows:
        ticker = r["Ticker"]
        weight = pct.get(ticker, "0.00%")
        html.append(
            "<tr>"
            f"<td>{ticker}</td>"
            f"<td>{fmt(r['Shares'], decimals=0)}</td>"
            f"<td>${fmt(r['Price'])}</td>"
            f"<td>${fmt(r['AvgCost'])}</td>"
            f"<td>${fmt(r['Value'])}</td>"
            f"<td>{('-' if r['PnL'] < 0 else '')}${fmt(abs(r['PnL']))}</td>"
            f"<td>{fmt(r['PnL_%'])}%</td>"
            f"<td>{weight}</td>"
            "</tr>"
        )

    html += [
        "</tbody></table>",
        "<div class='totals'>",
        "<div class='label'>Total Value</div>", f"<div>${fmt(totals['TotalValue'])}</div>",
        "<div class='label'>Total Cost</div>",  f"<div>${fmt(totals['TotalCost'])}</div>",
        "<div class='label'>Total PnL</div>",   f"<div>{('-' if totals['TotalPnL'] < 0 else '')}${fmt(abs(totals['TotalPnL']))}</div>",
        "<div class='label'>Total PnL %</div>", f"<div>{fmt(totals['TotalPnL_%'])}%</div>",
        "</div>",
        "</body></html>"
    ]

    HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    HTML_PATH.write_text("\n".join(html), encoding="utf-8")
    print(f"Wrote report → {HTML_PATH}")

if __name__ == "__main__":
    build_html()
