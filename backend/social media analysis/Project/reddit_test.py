import os
import praw
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Test – get top 5 posts from r/environment
for submission in reddit.subreddit("environment").hot(limit=5):
    print(submission.title)
