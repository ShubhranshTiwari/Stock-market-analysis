import pandas as pd
import plotly.express as px
import yfinance as yf
import datetime

# Hardcoded events data
events_data = [
    {
        "country": "China",
        "event": "COVID-19 Outbreak",
        "date": "2020-01-20",
        "description": "COVID-19 cases surge in Wuhan, China. Markets start to react globally.",
        "affected_tickers": ["AAPL", "MSFT", "SPY"],
        "impact": "High"
    },
    {
        "country": "Russia",
        "event": "Russia-Ukraine Conflict Escalation",
        "date": "2022-02-24",
        "description": "Russia invades Ukraine. Energy stocks surge, global indices drop.",
        "affected_tickers": ["XOM", "BP", "SPY"],
        "impact": "Severe"
    },
    {
        "country": "USA",
        "event": "Silicon Valley Bank Collapse",
        "date": "2023-03-10",
        "description": "SVB, a major tech-focused bank, collapses, sparking fear in the financial sector.",
        "affected_tickers": ["JPM", "QQQ", "XLF"],
        "impact": "Moderate"
    },
    {
        "country": "Saudi Arabia",
        "event": "OPEC Oil Production Cut",
        "date": "2023-04-02",
        "description": "OPEC+ announces surprise cut in oil output. Oil prices spike.",
        "affected_tickers": ["XOM", "CVX", "OXY"],
        "impact": "High"
    }
]

# Function to fetch stock data from Yahoo Finance
def fetch_stock_data(ticker):
    data = yf.download(ticker, start="2019-01-01", end=str(datetime.date.today()))
    return data

# Function to simulate the effect of events on stock prices
def simulate_event_impact(stock_data, event_date):
    event_date = pd.to_datetime(event_date)
    
    # Ensure the event_date exists in the stock data
    if event_date in stock_data.index:
        event_price = stock_data.loc[event_date]["Close"]
        
        # Select the future price changes from the event date onward
        future_prices = stock_data.loc[event_date:].iloc[1:]["Close"]
        
        # Calculate the percentage change (mean change for simplicity)
        future_change = future_prices.pct_change().mean()
        
        # Ensure that event_price and future_change are scalar values, not Series
        event_price = event_price.item() if isinstance(event_price, pd.Series) else event_price
        future_change = future_change.item() if isinstance(future_change, pd.Series) else future_change
        
        return event_price, future_change
    else:
        return None, None

# Function to display the geographic impact viewer
def geographic_impact_viewer(ticker):
    stock_data = fetch_stock_data(ticker)

    event_impact_details = []

    for event in events_data:
        event_date = event["date"]
        event_price, future_change = simulate_event_impact(stock_data, event_date)
        
        if event_price is not None:
            impact = f"Price at event: ${event_price:.2f}, Change in next few days: {future_change * 100:.2f}%"
        else:
            impact = "No data available for this date."
        
        event_impact_details.append({
            "Event": event["event"],
            "Country": event["country"],
            "Date": event["date"],
            "Impact": event["impact"],
            "Affected Tickers": ", ".join(event["affected_tickers"]),
            "Impact Details": impact
        })

    # Create a DataFrame to display the events
    impact_df = pd.DataFrame(event_impact_details)

    # Ensure that stock_data.index and stock_data['Close'] have matching lengths
    x_data = stock_data.index
    y_data = stock_data['Close'].squeeze()  # Flatten the 'Close' column to 1D

    # Plot the stock data
    fig = px.line(x=x_data, y=y_data, title=f"{ticker} Stock Price Over Time")
    fig.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
    fig.show()

    return impact_df

# Example usage
if __name__ == "__main__":
    ticker = 'AAPL'
    impact_df = geographic_impact_viewer(ticker)
    print(impact_df)
