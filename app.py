import streamlit as st
import pandas as pd
import time
from data_fetcher import fetch_live_data, compute_returns
from garch_model import fit_garch
from regime_detector import detect_regime
from utils import aggregate_market_volatility

st.title("Real-Time NIFTY 500 Volatility & Regime Dashboard")

symbols = pd.read_csv("nifty500_list.csv")["Symbol"].tolist()

refresh_rate = st.slider("Refresh Interval (seconds)", 10, 120, 30)

while True:
    data = fetch_live_data(symbols)
    returns = compute_returns(data)
    
    market_vol = aggregate_market_volatility(returns)
    market_return = returns.mean().mean()
    
    regime = detect_regime(market_vol, market_return)
    
    st.metric("Market Volatility", round(market_vol, 4))
    st.metric("Average Market Return", round(market_return, 4))
    st.metric("Current Regime", regime)
    
    st.write("Regime Meaning:")
    regime_map = {
        0: "Calm Growth",
        1: "Volatile Growth",
        2: "Correction",
        3: "Crisis"
    }
    
    st.success(regime_map[regime])
    
    time.sleep(refresh_rate)
    st.rerun()
