# utils.py
import os
import json
import math
from typing import Dict, Tuple, Iterable, Optional

import yfinance as yf
import pandas as pd


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_DIR = os.path.join(ROOT, "data")

# ---------------Load Positions-------------------
def load_positions():

    path = os.path.join(DATA_DIR, "positions.json")
    with open(path, "r") as f:
        obj = json.load(f)

    cash = float(obj.get("cash", 0.0))
    raw = obj.get("positions", {})
    if not raw:
        raise ValueError("No positions found in positions.json")

    positions = {}
    for tic, val in raw.items():
        if isinstance(val, dict):
            shares = float(val.get("shares", 0.0))
            avg_cost = val.get("avg_cost", None)
            avg_cost = float(avg_cost) if avg_cost is not None else None
        else:
            shares, avg_cost = float(val), None
        positions[tic] = {"shares": shares, "avg_cost": avg_cost}

    return cash, positions

# ---------------Shares Map-----------------
def shares_map(positions):
    shares = {}
    for tic, info in positions.items():
        shares[tic] = float(info.get("shares", 0.0))
    return shares

# --------------Latest Price-----------------

def latest_prices(tickers):
    prices = {}
    for tic in tickers:
        data = yf.Ticker(tic).history(period="1d", interval="1m")
        price = data["Close"].dropna().iloc[-1] if not data.empty else float('nan')
        prices[tic] = price
        
    return prices



    


