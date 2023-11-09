def tweet_schema(tweet) -> dict:
    return {
        "tweet_id" : str(tweet['_id']),
        "content" : tweet['content'],
        "created_at" : tweet['created_at'],
        "updated_at" : tweet['updated_at'],
        "by" : {'user_id' : tweet['by']['user_id'],
                "email": tweet['by']['email'],
                "desable": tweet['by']['desable'],
                "username": tweet['by']['username'],
                "first_name": tweet['by']['first_name'],
                "last_name": tweet['by']['last_name'],
                "birth_date": tweet['by']['birth_date']
                }
    }
    
def tweets_schema(tweets) -> list:
    return [tweet_schema(tweet) for tweet in tweets]