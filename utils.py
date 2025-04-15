import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from datetime import timedelta

@st.cache_data
def fetch_stock_data(ticker, start, end):
    try:
        df = yf.download(ticker, start=start, end=end)
        df.dropna(inplace=True)
        return df
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return pd.DataFrame()

@st.cache_data
def fetch_news_data(ticker, date):
    # Placeholder: Replace with actual logic if you get a news API later
    return pd.DataFrame()  # Returning empty df for now

def plot_stock_chart(df):
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df, x='Date', y='Close', ax=ax)
    ax.set_title('Stock Price Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price')
    st.pyplot(fig)
