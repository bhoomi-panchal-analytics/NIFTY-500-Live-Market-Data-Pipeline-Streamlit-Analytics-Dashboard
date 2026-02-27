def detect_regime(volatility, return_mean):
    
    if volatility < 1 and return_mean > 0:
        return 0  # Calm Growth
    
    elif volatility >= 1 and return_mean > 0:
        return 1  # Volatile Growth
    
    elif volatility >= 1 and return_mean <= 0:
        return 2  # Correction
    
    elif volatility >= 2 and return_mean < -0.01:
        return 3  # Crisis
