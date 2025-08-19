import yfinance as yf
import pandas as pd
import os
import json

from portfolio.scripts.utils import load_positions, shares_map, latest_prices

def get_percentages():
    cash, positions = load_positions()
    shares = shares_map(positions)                  
    prices = latest_prices(shares.keys())          

    # Total portfolio value (include cash)
    total = cash
    for tic, qty in shares.items():
        px = prices.get(tic, float('nan'))
        if px == px:                               
            total += px * qty

    # Weights per ticker
    percentages = {}
    for tic, qty in shares.items():
        px = prices.get(tic, float('nan'))
        if px == px and total > 0:
            weight = round((px * qty) / total * 100, 2)
        else:
            weight = 0.0
        percentages[tic] = f"{weight:.2f}%"

    return total, percentages

def main():
    total, pct = get_percentages()
    print(f"Total (incl. cash): {total:.2f}")
    print(pct)

if __name__ == "__main__":
    main()







