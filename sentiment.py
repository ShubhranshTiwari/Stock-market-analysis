from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
# import snscrape.modules.twitter as sntwitter
import pandas as pd
import re

def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    return "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"

def fetch_news(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, 'html.parser')

    news = []
    for item in soup.find_all('h3'):
        title = item.get_text()
        sentiment = get_sentiment(title)
        news.append({'text': title, 'sentiment': sentiment})
    return pd.DataFrame(news)

# def fetch_tweets(query, count=20):
#     tweets = []
#     for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{query} lang:en').get_items()):
#         if i >= count:
#             break
#         clean_text = re.sub(r'http\S+|@\w+|#\w+', '', tweet.content)
#         sentiment = get_sentiment(clean_text)
#         tweets.append({'text': clean_text, 'sentiment': sentiment})
#     return tweets
