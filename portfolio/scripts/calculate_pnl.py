from portfolio.scripts.utils import load_positions, latest_prices

def get_pnl():
    cash, positions = load_positions()
    prices = latest_prices(positions.keys())

    rows = []
    total_value = cash
    total_cost = cash

    for tic, info in positions.items():
        shares = info["shares"]
        avg_cost = info["avg_cost"]

        price = prices.get(tic, float('nan'))
        value = price * shares if price == price else 0.0  # NaN check
        cost_basis = avg_cost * shares if avg_cost is not None else 0.0
        pnl = value - cost_basis
        pnl_pct = (pnl / cost_basis * 100) if cost_basis > 0 else 0.0

        total_value += value
        total_cost += cost_basis

        rows.append({
            "Ticker": tic,
            "Shares": shares,
            "Price": price,
            "AvgCost": avg_cost,
            "Value": value,
            "CostBasis": cost_basis,
            "PnL": pnl,
            "PnL_%": pnl_pct
        })

    totals = {
        "TotalValue": total_value,
        "TotalCost": total_cost,
        "TotalPnL": total_value - total_cost,
        "TotalPnL_%": ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0.0
    }

    return rows, totals

def main():
    rows, totals = get_pnl()

    for r in rows:
        print(f"{r['Ticker']:5} | sh:{r['Shares']:>5} | px:{r['Price']:.2f} | "
              f"cost:{r['AvgCost']:.2f} | val:{r['Value']:.2f} | "
              f"PnL:{r['PnL']:.2f} ({r['PnL_%']:.2f}%)")
    print("\nTotals:", totals)

if __name__ == "__main__":
    main()