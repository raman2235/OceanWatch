import os
import tweepy
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Credentials
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_KEY_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Tweepy client (v2)
client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=api_key,
                       consumer_secret=api_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

# Example: search recent tweets about "tsunami"
query = "tsunami lang:en -is:retweet"
tweets = client.search_recent_tweets(query=query, max_results=10)

for tweet in tweets.data:
    print(tweet.text)
