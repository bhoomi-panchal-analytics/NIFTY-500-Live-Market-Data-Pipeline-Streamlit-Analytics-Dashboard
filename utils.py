import numpy as np

def aggregate_market_volatility(returns_df):
    vol_list = []
    for col in returns_df.columns:
        vol_list.append(returns_df[col].std())
    return np.mean(vol_list)
