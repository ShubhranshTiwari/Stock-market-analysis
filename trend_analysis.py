import pandas as pd

def detect_trend(data: pd.DataFrame, short_window=20, long_window=50) -> str:
    """
    Analyze trend based on moving averages.
    Returns a trend summary.
    """
    data = data.copy()

    # Calculate moving averages
    data['MA_short'] = data['Close'].rolling(window=short_window).mean()
    data['MA_long'] = data['Close'].rolling(window=long_window).mean()

    latest_short = data['MA_short'].iloc[-1]
    latest_long = data['MA_long'].iloc[-1]

    trend = ""
    if pd.isna(latest_short) or pd.isna(latest_long):
        trend = "Not enough data to determine trend."
    elif latest_short > latest_long:
        trend = "🔼 Uptrend detected: Short-term MA is above long-term MA."
    elif latest_short < latest_long:
        trend = "🔻 Downtrend detected: Short-term MA is below long-term MA."
    else:
        trend = "➡️ Sideways trend: Short-term and long-term MAs are similar."

    # Optional: Add slope-based strength detection
    slope_short = data['MA_short'].iloc[-1] - data['MA_short'].iloc[-5]
    slope_long = data['MA_long'].iloc[-1] - data['MA_long'].iloc[-5]

    if "Uptrend" in trend and slope_short > 0 and slope_long > 0:
        trend += " Trend is strengthening."
    elif "Downtrend" in trend and slope_short < 0 and slope_long < 0:
        trend += " Trend is weakening further."
    elif "Sideways" in trend:
        trend += " Market may be consolidating."

    return trend
