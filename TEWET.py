import tweepy

# Set up Twitter API client
client = tweepy.Client(bearer_token='your_bearer_token')

# Search for tweets containing 'brainrot'
tweets = client.search_recent_tweets(query="brainrot", max_results=100)

# Collect tweet text
tweet_texts = [tweet.text for tweet in tweets.data]

# Save tweets to file
with open("brainrot_data.txt", "a") as file:
    file.write("\n".join(tweet_texts))
