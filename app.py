# app.py
import streamlit as st
import pandas as pd
from data_fetcher import get_stock_data
from stock_statistics import calculate_basic_stats
from visualizer import plot_price, plot_with_moving_averages
from trend_analysis import detect_trend
import matplotlib.pyplot as plt
import time
import yfinance as yf
from Investor_time_machine import investor_time_machine

st.set_page_config(page_title="📈 Stock Market Analyzer", layout="wide")

st.title("📊 Stock Market Analysis Dashboard")

st.sidebar.header("User Inputs")
ticker = st.sidebar.text_input("Stock Ticker (e.g. AAPL)", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Price Chart",
    "📊 Moving Averages", 
    "📉 Trend Analysis",
    "📋 Statistics", 
    "🔴 Live Ticker",
    "🕰️ Investor Time Machine"
])
df = get_stock_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

if st.sidebar.button("Analyze"):
    with st.spinner("Fetching data..."):
        df = get_stock_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    if df.empty:
        st.error("No data found. Please check the ticker and date range.")
    else:
        st.success("Data successfully loaded!")

        with tab1:
            st.subheader("Closing Price Chart")
            st.pyplot(plot_price(df, ticker))

        with tab4:
            st.subheader("📋 Basic Statistics Summary")
            stats = calculate_basic_stats(df)

            col1, col2, col3 = st.columns(3)
    
            with col1:
                st.metric(label="🔼 Max Price", value=f"${stats['Max Price']:.2f}")
                st.metric(label="📅 Start Date", value=stats['Start Date'])
    
            with col2:
                st.metric(label="🔽 Min Price", value=f"${stats['Min Price']:.2f}")
                st.metric(label="📅 End Date", value=stats['End Date'])
    
            with col3:
                st.metric(label="⚖️ Average Price", value=f"${stats['Average Price']:.2f}")
                st.metric(label="📊 Total Days", value=stats['Total Days'])


        with tab3:
            st.subheader("Trend Detection")
            trend = detect_trend(df)
            st.info(trend)
            # def show_trend_analysis(df, ticker):
            #     st.markdown("## 📈 Trend Analysis")
            #     st.markdown("Identify market direction using short and long-term moving averages.")

            #     if df.empty or 'Close' not in df.columns:
            #         st.warning("⚠️ Dataframe is empty or missing 'Close' column.")
            #         return

            #     # Ensure datetime index
            #     if not df.index.inferred_type == 'datetime64':
            #         df.index = pd.to_datetime(df.index)

            #     # Detect trend summary
            #     trend_summary = detect_trend(df)
            #     st.markdown(
            #         f"""
            #         <div style='background-color:#f0f2f6; padding:15px; border-radius:10px; margin-bottom:20px;'>
            #             <h4 style='color:#3366cc;'>🧠 Trend Insight</h4>
            #             <p style='font-size:16px; color:#444;'>{trend_summary}</p>
            #         </div>
            #         """,
            #         unsafe_allow_html=True
            #     )

            #     # Calculate MAs
            #     df['MA_20'] = df['Close'].rolling(window=20).mean()
            #     df['MA_50'] = df['Close'].rolling(window=50).mean()

            #     # Debug check
            #     st.write("🔍 Latest MA values", df[['Close', 'MA_20', 'MA_50']].tail())

            #     # Plot
            #     fig = go.Figure()
            #     fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price', line=dict(color='#0077b6')))
            #     fig.add_trace(go.Scatter(x=df.index, y=df['MA_20'], mode='lines', name='20-day MA', line=dict(color='orange')))
            #     fig.add_trace(go.Scatter(x=df.index, y=df['MA_50'], mode='lines', name='50-day MA', line=dict(color='green')))

            #     fig.update_layout(
            #         title=f"{ticker} - Trend Analysis",
            #         xaxis_title="Date",
            #         yaxis_title="Price (USD)",
            #         template="plotly_white",
            #         height=450,
            #         margin=dict(t=40, b=30),
            #         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            #     )

            #     st.plotly_chart(fig, use_container_width=True)


        with tab2:
            st.subheader("Price with Moving Averages")
            st.pyplot(plot_with_moving_averages(df, ticker))

with tab5:
    st.subheader(f"🔴 Live Price Ticker: {ticker.upper()}")
    interval = st.slider("Update interval (seconds)", 1, 30, 5)

    live_placeholder = st.empty()
    chart_placeholder = st.empty()

    if st.button("Start Live Updates"):
        for i in range(100):  # You can increase this number
            try:
                stock = yf.Ticker(ticker)
                latest_data = stock.history(period="1d", interval="1m")
                latest_price = latest_data['Close'].iloc[-1]

                live_placeholder.metric(label="Current Price", value=f"${latest_price:.2f}")

                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(latest_data.index, latest_data['Close'], color='orange')
                ax.set_title(f"{ticker.upper()} Live Price (1m Interval)")
                ax.set_xlabel("Time")
                ax.set_ylabel("Price")
                ax.grid(True)
                chart_placeholder.pyplot(fig)

                time.sleep(interval)
            except Exception as e:
                st.error(f"Error fetching live data: {e}")
                break

with tab6:
    investor_time_machine(ticker)

# with tab6:
#     st.subheader(f"📰 News Sentiment Analysis for {ticker.upper()}")

#     st.write("Analyzing recent headlines from Yahoo Finance...")
    
#     news_df = fetch_news(ticker)

#     if news_df.empty:
#         st.warning("No news headlines found for sentiment analysis.")
#     else:
#         # --- Stats Summary ---
#         avg_sentiment = news_df['Sentiment'].mean()
#         sentiment_label = "Positive" if avg_sentiment > 0.1 else "Negative" if avg_sentiment < -0.1 else "Neutral"
#         sentiment_color = "🟢" if sentiment_label == "Positive" else "🔴" if sentiment_label == "Negative" else "🟡"

#         st.markdown(f"### Overall News Sentiment: {sentiment_color} **{sentiment_label}**")
#         st.write(f"Average Sentiment Score: `{avg_sentiment:.3f}`")

#         # --- Sentiment Pie Chart ---
#         sentiment_counts = news_df['Sentiment'].apply(
#             lambda x: 'Positive' if x > 0.1 else 'Negative' if x < -0.1 else 'Neutral'
#         ).value_counts()

#         fig_pie, ax_pie = plt.subplots()
#         ax_pie.pie(
#             sentiment_counts,
#             labels=sentiment_counts.index,
#             autopct='%1.1f%%',
#             startangle=140,
#             colors=["#66bb6a", "#ef5350", "#ffee58"]
#         )
#         ax_pie.set_title("Sentiment Distribution of News Headlines")
#         st.pyplot(fig_pie)

#         # --- Show Recent Headlines in Table ---
#         st.markdown("### 📰 Latest Headlines")
#         st.dataframe(news_df[['Date', 'Headline', 'Sentiment']].sort_values(by="Date", ascending=False), use_container_width=True)

#         # --- Optional: Bar chart of sentiment scores over time ---
#         chart_data = news_df[['Date', 'Sentiment']].groupby('Date').mean().reset_index()

#         st.markdown("### 📊 Daily Average Sentiment Trend")
#         fig_line, ax_line = plt.subplots()
#         ax_line.plot(chart_data['Date'], chart_data['Sentiment'], marker='o', linestyle='-', color='#42a5f5')
#         ax_line.axhline(y=0, color='gray', linestyle='--')
#         ax_line.set_xlabel("Date")
#         ax_line.set_ylabel("Average Sentiment")
#         ax_line.set_title("Sentiment Over Time")
#         ax_line.grid(True)
#         st.pyplot(fig_line)


# with tab6:
#     st.subheader(f"📰 News Sentiment Analysis for {ticker.upper()}")

#     st.write("Analyzing recent headlines from Yahoo Finance...")
    
#     news_data = fetch_news(ticker)

#     if not news_data:
#         st.warning("No news headlines found. Try another ticker.")
#     else:
#         df_news = pd.DataFrame(news_data)
#         sentiment_counts = df_news['sentiment'].value_counts()

#         st.write("### 🔍 Sentiment Breakdown")
#         st.bar_chart(sentiment_counts)

#         st.write("### 🗞️ Recent Headlines")
#         for _, row in df_news.iterrows():
#             st.markdown(f"- *{row['text']}* — **{row['sentiment']}**")
