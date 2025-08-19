from portfolio.scripts import calculate_percentages
from portfolio.scripts import calculate_pnl
from portfolio.scripts import web_report
from portfolio.scripts import web_dashboard
import webbrowser
import os

def portfolio_check():

    print('Portfolio Check\n')

    total, pct = calculate_percentages.get_percentages()
    rows, totals = calculate_pnl.get_pnl()

    for r in rows:
        ticker = r['Ticker']
        percentage = pct[ticker]
        print(f"{r['Ticker']:>5} | sh:{r['Shares']:>5} | px:{r['Price']:>6.2f} | "
              f"cost:{r['AvgCost']:>6.2f} | val:{r['Value']:>8.2f} | "
              f"PnL:{r['PnL']:>8.2f} ({r['PnL_%']:>7.2f}%) | "
              f"wt:{percentage:>10}"
              )
        
    print('\n')
    for key, value in totals.items():
        # Last Column Special
        if key.endswith("_%"):  
            print(f"{key:15}: {value:>10.2f}%")
        else:  
            print(f"{key:15}: {value:>10.2f}")

if __name__ == "__main__":
    portfolio_check()
    web_report.build_html()
    html_path = os.path.abspath("/Users/yuzekai/Desktop/Zekai Investment/portfolio/data/portfolio_report.html")
    webbrowser.open(f"file://{html_path}")
    # web_dashboard.app.run(debug=True)