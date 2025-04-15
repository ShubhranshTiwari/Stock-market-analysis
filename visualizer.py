# import matplotlib.pyplot as plt
# import pandas as pd

# def plot_price(data: pd.DataFrame, ticker: str):
#     """
#     Plot closing price.
#     """
#     # Inside plot_price
#     fig, ax = plt.subplots()
#     ax.plot(data['Date'], data['Close'], label='Close Price')
#     plt.figure(figsize=(10, 5))
#     plt.plot(data['Date'], data['Close'], label='Close Price')
#     plt.title(f"{ticker} Closing Price")
#     plt.xlabel("Date")
#     plt.ylabel("Price (USD)")
#     plt.legend()
#     plt.grid()
#     plt.tight_layout()
#     return fig



# def plot_with_moving_averages(data: pd.DataFrame, ticker: str, ma_days=[20, 50]):
#     """
#     Plot price with moving averages.
#     """
#     # Inside plot_price
#     fig, ax = plt.subplots()
#     ax.plot(data['Date'], data['Close'], label='Close Price')
#     plt.figure(figsize=(12, 6))
#     plt.plot(data['Date'], data['Close'], label='Close Price')

#     for ma in ma_days:
#         data[f"MA_{ma}"] = data['Close'].rolling(window=ma).mean()
#         plt.plot(data['Date'], data[f"MA_{ma}"], label=f"{ma}-Day MA")

#     plt.title(f"{ticker} Price with Moving Averages")
#     plt.xlabel("Date")
#     plt.ylabel("Price (USD)")
#     plt.legend()
#     plt.grid()
#     plt.tight_layout()
#     return fig
import matplotlib.pyplot as plt
import pandas as pd

def plot_price(data: pd.DataFrame, ticker: str):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data['Date'], data['Close'], label='Close Price', color='blue')
    ax.set_title(f'{ticker.upper()} Closing Price', fontsize=14)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.grid(True)
    ax.legend()
    return fig

def plot_with_moving_averages(data: pd.DataFrame, ticker: str, short_window=20, long_window=50):
    data = data.copy()
    data['MA_short'] = data['Close'].rolling(window=short_window).mean()
    data['MA_long'] = data['Close'].rolling(window=long_window).mean()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data['Date'], data['Close'], label='Close Price', color='blue')
    ax.plot(data['Date'], data['MA_short'], label=f'{short_window}-Day MA', color='green')
    ax.plot(data['Date'], data['MA_long'], label=f'{long_window}-Day MA', color='red')
    ax.set_title(f'{ticker.upper()} Price with Moving Averages', fontsize=14)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.grid(True)
    ax.legend()
    return fig
