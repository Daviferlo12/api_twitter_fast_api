def tweet_schema(tweet) -> dict:
    return {
        "tweet_id" : str(tweet['_id']),
        "content" : tweet['content'],
        "created_at" : tweet['created_at'],
        "updated_at" : tweet['updated_at'],
        "by" : tweet['by']
    }
    
def tweets_schema(tweets) -> list:
    return [tweet_schema(tweet) for tweet in tweets]