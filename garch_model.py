from arch import arch_model
import numpy as np

def fit_garch(returns):
    model = arch_model(returns * 100, vol='Garch', p=1, q=1)
    res = model.fit(disp='off')
    forecast = res.forecast(horizon=1)
    volatility = np.sqrt(forecast.variance.values[-1, :][0])
    return volatility
