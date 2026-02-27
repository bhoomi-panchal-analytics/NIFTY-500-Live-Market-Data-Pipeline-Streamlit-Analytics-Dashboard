import yfinance as yf
import pandas as pd

def fetch_live_data(symbols, period="6mo", interval="1d"):
    data = yf.download(symbols, period=period, interval=interval, group_by="ticker", auto_adjust=True)
    return data

def compute_returns(data):
    returns = {}
    for symbol in data.columns.levels[0]:
        if "Close" in data[symbol]:
            returns[symbol] = data[symbol]["Close"].pct_change().dropna()
    return pd.DataFrame(returns)
