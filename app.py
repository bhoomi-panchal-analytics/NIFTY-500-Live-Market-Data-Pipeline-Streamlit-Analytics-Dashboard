import streamlit as st
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh

from data_fetcher import fetch_live_data, compute_returns
from garch_model import fit_garch
from regime_detector import detect_regime

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="NIFTY 500 Live Volatility & Regime Dashboard",
    layout="wide"
)

st.title("Real-Time NIFTY 500 Volatility & Regime Detection")
st.markdown("Using GARCH Volatility Forecasting + 4-Regime Classification")

# ---------------------------
# Sidebar Controls
# ---------------------------
st.sidebar.header("Settings")

refresh_interval = st.sidebar.slider(
    "Auto Refresh Interval (seconds)",
    min_value=30,
    max_value=600,
    value=120,
    step=30
)

# Convert to milliseconds for autorefresh
st_autorefresh(interval=refresh_interval * 1000, key="refresh")

# ---------------------------
# Load Symbols
# ---------------------------
@st.cache_data(ttl=300)
def load_symbols():
    df = pd.read_csv("nifty500_list.csv")
    return df["Symbol"].dropna().tolist()

symbols = load_symbols()

# ---------------------------
# Fetch Market Data
# ---------------------------
@st.cache_data(ttl=300)
def load_market_data(symbols):
    return fetch_live_data(symbols, period="6mo", interval="1d")

data = load_market_data(symbols)

if data.empty:
    st.error("No data fetched. Check internet or ticker symbols.")
    st.stop()

# ---------------------------
# Compute Returns
# ---------------------------
returns = compute_returns(data)

if returns.empty:
    st.warning("Not enough return data available.")
    st.stop()

# ---------------------------
# Aggregate Market Volatility
# ---------------------------
market_vol_list = []
for col in returns.columns:
    try:
        vol = fit_garch(returns[col].dropna())
        market_vol_list.append(vol)
    except:
        continue

if len(market_vol_list) == 0:
    st.warning("GARCH failed on all assets.")
    st.stop()

market_volatility = np.mean(market_vol_list)
market_return = returns.mean().mean()

# ---------------------------
# Detect Regime
# ---------------------------
current_regime = detect_regime(market_volatility, market_return)

regime_map = {
    0: "Calm Growth",
    1: "Volatile Growth",
    2: "Correction",
    3: "Crisis"
}

# ---------------------------
# Display Metrics
# ---------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Market Volatility (GARCH Forecast)", round(market_volatility, 4))
col2.metric("Average Market Return", round(market_return, 4))
col3.metric("Current Regime", regime_map.get(current_regime, "Unknown"))

# ---------------------------
# Regime Explanation
# ---------------------------
st.subheader("Regime Description")

if current_regime == 0:
    st.success("Low volatility + Positive returns → Stable Bull Market")
elif current_regime == 1:
    st.info("High volatility + Positive returns → Uncertain Growth Phase")
elif current_regime == 2:
    st.warning("High volatility + Negative returns → Market Correction")
elif current_regime == 3:
    st.error("Extreme volatility + Large negative returns → Crisis")
else:
    st.write("Regime not determined.")

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.caption("Live data via Yahoo Finance API | Volatility via GARCH(1,1)")
