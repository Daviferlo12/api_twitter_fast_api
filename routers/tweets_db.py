#PYTHON
from typing import List
from uuid import UUID
import json
import pymongo

# FAST API
from fastapi import APIRouter
from fastapi import(
    status, Body, Path, HTTPException
)
from fastapi.params import Depends

#MODELS
# from models.User import User
from db.models.Tweet import Tweet
from db.models.User import User

# DB
from db.con import db_client

# SCHEMAS
from db.schemas.tweet import tweet_schema, tweets_schema

router = APIRouter(
                    prefix="/tweets",
                    tags=["Tweets"],
                    responses={404: {'Message' : 'Error : Not Found'}}
                )

#LOGIN FUNCTIONS
from routers.jwt_autentication_db import current_user



## TWEETS

### Get all tweets
@router.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets"
)
def show_all_tweets():
    
    """
        **Show all Tweets**

    This endpoint shows all tweets in the app.

    Parameters:
        -

    Returns a JSON list with all tweets in the app, with the following structure:
    
    - tweet_id: UUID
    - content: str
    - created_at: str
    - updated_at: str
    - updated_at: User
    """
    return tweets_schema(db_client.local.tweets.find())


### Get a tweet by ID
@router.get(
    path="/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Get a tweet"
)
def get_a_tweet_by_id(tweet_id : UUID = Path(
                                    ...,
                                    title="Tweet ID",
                                    example="7fa85f64-5717-4562-b3fc-2c963f66afn0"
                                )):
    
    """
    Get a Tweet
    
    This is an endpoint to get an especific tweet
    
    Parameters:
    - tweet_id : UUID

    Returns a json with the basic tweet information:
    - tweet_id : UUID
    - content : str
    - created_at : datetime 
    - updated_at : Optional[datetime]
    - by: User  
    """
    return search_tweet('_id', tweet_id)


# Get a tweets by a keyword in content
@router.get(
    path="/search/",
    response_model=list[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Get tweets by keyword"
)
def get_tweets_by_keyword(keyword : str):
    
    """
    Get tweets by a keyword
    
    This is an endpoint to get all tweets that matches with a keyword in the contect of the tweet
    
    Parameters:
    - keyword : str

    Returns a json with the basic tweet information:
    - tweet_id : UUID
    - content : str
    - created_at : datetime 
    - updated_at : Optional[datetime]
    - by: User  
    """
    return tweets_schema(search_tweet_by_keyword('content', keyword))



# Get tweets by username

@router.get(
    path="/search/username/",
    response_model=list[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Get tweets by keyword"
)
def get_tweets_by_username(username : str):
    
    """
    Get tweets by a username
    
    This is an endpoint to get all tweets that matches with a username
    
    Parameters:
    - username : str

    Returns a json with the basic tweet information:
    - tweet_id : UUID
    - content : str
    - created_at : datetime 
    - updated_at : Optional[datetime]
    - by: User  
    """
    return tweets_schema(search_tweet_by_keyword('by.username',username))


### Create a tweet
@router.post(
    path="/create",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Create a tweet"
)
# def post(tweet : Annotated[Tweet, Depends(current_user)] = Body(...)):
def post(tweet : Tweet = Body(...), user : User = Depends(current_user)):
    """
    Create a tweet
    
    In this endpoint you can create a new tweet
    
    Parameters:
    - Reques body parameter:
        - tweet : Tweet
        
    Return a json with the basic informationb of the tweet:
    - tweet_id : UUID
    - content : str
    - created_at : dateTime
    - updated_at : Optional[dateTime]
    - by : User
    """
    tweet_dict = dict(tweet)
    tweet_dict['_id'] = tweet_dict['tweet_id']
    tweet_dict['by'] = dict(tweet_dict['by'])
    del tweet_dict['tweet_id']
    
    #Insert the tweet Object and get its ID
    id = db_client.local.tweets.insert_one(tweet_dict).inserted_id
    
    # Get the inserted object using schema
    inserted_tweet = tweet_schema(db_client.local.tweets.find_one({"_id" : id}))
        
    return inserted_tweet


### Update a tweet
@router.put(
    path="/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary= "Update a tweet"
)
def update_a_tweet(tweet : Tweet = Body(
                       ...,
                       title="Tweet"
                   ), user : User = Depends(current_user)):
    """
    **Update a Tweet**
    
    This is an endpoint to update an especific tweet
    
    Path Parameter:
    - tweet_id : UUID
    
    Body parameter:
    - tweet : tweet

    Return a json with the basic informationb of the tweet:
    - tweet_id : UUID
    - content : str
    - created_at : dateTime
    - updated_at : Optional[dateTime]
    - by : User
        
    """
    tweet_dict = dict(tweet)
    tweet_dict["_id"] = tweet_dict['tweet_id']
    tweet_dict['by'] = dict(tweet_dict['by'])
    del tweet_dict["tweet_id"]
    
    try:
        db_client.local.tweets.find_one_and_replace({'_id' : tweet.tweet_id}, tweet_dict)
    except:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User did not update correctly..."
        )
            
    return search_tweet('_id', tweet.tweet_id)


### Delete a tweet
@router.delete(
    path="/{tweet_id}/delete",
    # response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary= "Delete a tweet"
)
def delete_a_tweet(tweet_id : UUID = Path(
                                    ...,
                                    title="Tweet ID",
                                    example="7fa85f64-5717-4562-b3fc-2c963f66afn0"
                                ), user : User = Depends(current_user)):
    
    """
    Delete a tweet
    
    This is an endpoint to delete a tweet
    
    Parameters:
    - tweet_id : UUID

    Returns a HTTP response 200 if the tweet was correctly deleted
        
    """ 
    result = db_client.local.tweets.find_one_and_delete({'_id' : tweet_id})
    
    if not result:     
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error, tweet not eliminated"
        )
    
    return status.HTTP_200_OK
        
        
        

# Search a tweet by a parameter

def search_tweet(field : str, key): 
    try:
        tweet = tweet_schema(db_client.local.tweets.find_one({field : key}))
        return Tweet(**tweet)
    except:
        return {'error' : 'User not found'}
    
    
def search_tweet_by_keyword(field, key_word): 
    try:
        result = db_client.local.tweets.find({ field : { "$regex": key_word, "$options" : 'i' } })
        return result 
    except:
        return {'error' : 'No coincidences'}
    