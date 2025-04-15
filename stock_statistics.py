import pandas as pd

# def calculate_basic_stats(data: pd.DataFrame) -> dict:
#     """
#     Calculate basic statistics on the stock data.
#     Returns a dictionary of stats.
#     """
#     stats = {}

#     # Calculate daily returns
#     data['Daily Return'] = data['Close'].pct_change()

#     stats['Start Date'] = str(data['Date'].iloc[0].date())
#     stats['End Date'] = str(data['Date'].iloc[-1].date())
#     stats['Total Days'] = len(data)

#     stats['Initial Price'] = round(data['Close'].iloc[0], 2)
#     stats['Final Price'] = round(data['Close'].iloc[-1], 2)
#     stats['Overall Change (%)'] = round(((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100, 2)

#     stats['Mean Price'] = round(data['Close'].mean(), 2)
#     stats['Median Price'] = round(data['Close'].median(), 2)
#     stats['Std Dev'] = round(data['Close'].std(), 2)

#     stats['Max Price'] = round(data['Close'].max(), 2)
#     stats['Min Price'] = round(data['Close'].min(), 2)

#     stats['Best Day Return (%)'] = round(data['Daily Return'].max() * 100, 2)
#     stats['Worst Day Return (%)'] = round(data['Daily Return'].min() * 100, 2)

#     return stats

def calculate_basic_stats(data):
    # Ensure correct types and no NaNs
    max_price = float(data['Close'].max())
    min_price = float(data['Close'].min())
    avg_price = float(data['Close'].mean())
    start_date = data['Date'].iloc[0]
    end_date = data['Date'].iloc[-1]
    total_days = int(len(data))

    return {
        "Max Price": max_price,
        "Min Price": min_price,
        "Average Price": avg_price,
        "Start Date": start_date.strftime('%Y-%m-%d'),
        "End Date": end_date.strftime('%Y-%m-%d'),
        "Total Days": total_days
    }



def print_stats(stats: dict):
    """
    Print the stats in a readable format.
    """
    print("\n📊 Basic Stock Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")
