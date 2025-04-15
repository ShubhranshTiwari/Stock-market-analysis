import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
from utils import fetch_stock_data, fetch_news_data, plot_stock_chart


def fetch_stock_data(ticker, start_date, end_date):
    # Fetch stock data between the two dates
    df = yf.download(ticker, start=start_date, end=end_date)
    return df

def fetch_news_data(ticker, date):
    # Scrape news articles for the specific date (using BeautifulSoup for news scraping)
    query = f"{ticker} stock news {date.strftime('%Y-%m-%d')}"
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    
    # Scrape the news headlines from the Google News search results page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all('div', class_='BVG0Nb')

    news_list = []
    for headline in headlines[:5]:  # Only fetch top 5 headlines
        news_text = headline.get_text()
        sentiment = TextBlob(news_text).sentiment.polarity  # Perform sentiment analysis
        news_list.append({
            "text": news_text,
            "sentiment": sentiment
        })
    
    return pd.DataFrame(news_list)

def plot_stock_chart(stock_df, title="Stock Price Chart"):
    # Plot the stock price chart
    fig, ax = plt.subplots()
    ax.plot(stock_df['Date'], stock_df['Close'], label="Close Price", color="blue")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title(title)
    ax.legend()
    st.pyplot(fig)

# Main Streamlit UI
def investor_time_machine(ticker):
    st.title(f"🕰️ Investor Time Machine - {ticker.upper()}")
    st.markdown("Travel back in time and predict the market like a pro investor!")

    selected_date = st.date_input("🔎 Choose a historical date", datetime(2020, 1, 1))
    start_date = datetime(2000, 1, 1)
    end_date = selected_date

    stock_df = fetch_stock_data(ticker, start_date, end_date)
    stock_df['Date'] = stock_df.index

    st.subheader(f"📈 Stock Price History up to {selected_date}")
    plot_stock_chart(stock_df)

    # Show news if any
    news_df = fetch_news_data(ticker, selected_date)
    if not news_df.empty:
        st.subheader("📰 Top News That Day")
        for i, row in news_df.head(3).iterrows():
            st.info(f"**•** {row['text']}")

    st.markdown("### 🤔 Your Prediction:")
    prediction = st.radio("What do you think will happen in the next 7 days?", 
                          ('Stock Price will go Up', 'Stock Price will go Down', 'Stock Price will stay Flat'))

    if st.button("🕹️ Predict and Reveal Outcome!"):
        future_date = selected_date + timedelta(days=7)
        future_stock_df = fetch_stock_data(ticker, selected_date, future_date)

        if future_stock_df.empty:
            st.error("No data available for the next week.")
            return

        try:
            start_price = future_stock_df['Close'].iloc[0].item()
            end_price = future_stock_df['Close'].iloc[-1].item()
            change = end_price - start_price
            percent_change = (change / start_price) * 100

            # Determine actual direction
            if change > 0:
                actual_direction = "Up"
                emoji = "📈"
            elif change < 0:
                actual_direction = "Down"
                emoji = "📉"
            else:
                actual_direction = "Flat"
                emoji = "➖"

            st.markdown("---")
            col1, col2 = st.columns(2)
            col1.metric("📊 Start Price", f"${start_price:.2f}")
            col2.metric("🎯 End Price", f"${end_price:.2f}", f"{percent_change:.2f}%")

            st.markdown(f"### 🧭 Market actually moved: **{actual_direction} {emoji}**")

            # Evaluate prediction
            prediction_map = {
                'Stock Price will go Up': 'Up',
                'Stock Price will go Down': 'Down',
                'Stock Price will stay Flat': 'Flat'
            }

            if prediction_map[prediction] == actual_direction:
                st.success("✅ Great job! Your prediction was spot on! 🎉")
                st.balloons()
            else:
                st.error(f"❌ Oops! You predicted **{prediction_map[prediction]}**, but it went **{actual_direction}**.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
# Streamlit interface
if __name__ == "__main__":
    ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
    investor_time_machine(ticker)
