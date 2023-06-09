#PYTHON
from uuid import UUID
import json

# FAST API
from fastapi import APIRouter
from fastapi import(
    status, Body, Path, HTTPException
)

#MODELS
from models.User import User
from models.UserLogin import UserLogin
from models.UserBase import UserBase
from models.Tweet import Tweet
from models.UserRegister import UserRegister

router = APIRouter(
                    prefix="/tweets",
                    tags=["Tweets"],
                    responses={404: {'Message' : 'Error : Not Found'}}
                )



## TWEETS

### Get a tweet
@router.get(
    path="/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Get a tweet"
)
def show_tweet(tweet_id : UUID = Path(
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
    with open("tweets.json", mode="r", encoding="utf-8") as file:
        result = json.loads(file.read())
        
        for tweet in result:
            if tweet['tweet_id'] == str(tweet_id):             
                return tweet
                
                
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "This tweet does not exist..."
        )


### Create a tweet
@router.post(
    path="/create",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Create a tweet"
)
def post(tweet : Tweet = Body(...)):
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
    with open("tweets.json", mode="r+", encoding="utf-8") as file:
        resutls = json.loads(file.read())
        
        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str(tweet_dict['tweet_id'])
        tweet_dict['created_at'] = str(tweet_dict["created_at"])
        tweet_dict['updated_at'] = str(tweet_dict["updated_at"])
        
        tweet_dict['by']['user_id'] = str(tweet_dict['by']['user_id'])
        tweet_dict['by']['birth_date'] = str(tweet_dict['by']['birth_date'])
        
        resutls.append(tweet_dict)
        file.seek(0)
        file.write(json.dumps(resutls))
        
        return tweet


### Update a tweet
@router.put(
    path="/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary= "Update a tweet"
)
def update_a_tweet(tweet_id : UUID = Path(
                                    ...,
                                    title="Tweet ID",
                                    example="7fa85f64-5717-4562-b3fc-2c963f66afn0"
                                ),
                   tweet : Tweet = Body(
                       ...,
                       title="Tweet"
                   )):
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
    with open('tweets.json', mode="r+", encoding="utf-8") as file:
        
        results = json.loads(file.read())
        
        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str(tweet.tweet_id)
        tweet_dict['content'] = tweet.content
        tweet_dict['created_at'] = str(tweet.created_at)
        tweet_dict['updated_at'] = str(tweet.updated_at)
        tweet_dict['by']['user_id'] = str(tweet.by.user_id)
        tweet_dict['by']['email'] = tweet.by.email
        tweet_dict['by']['first_name'] = tweet.by.first_name
        tweet_dict['by']['last_name'] = tweet.by.last_name
        tweet_dict['by']['birth_date'] = str(tweet.by.birth_date)

        for tweet in results:
            if tweet['tweet_id'] == str(tweet_id):
                
                results[results.index(tweet)] = tweet_dict
                
                # break
                with open('tweets.json', mode="w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                    return tweet
            
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sorry, tweet no found.."
        )


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
                                )):
    
    """
    Delete a tweet
    
    This is an endpoint to delete a tweet
    
    Parameters:
    - tweet_id : UUID

    Returns a HTTP response 200 if the tweet was correctly deleted
        
    """
    with open('tweets.json', mode="r+", encoding="utf-8") as file:
        
        results = json.loads(file.read())
        
        for tweet in results:
            if tweet['tweet_id'] == str(tweet_id):
                results.remove(tweet)
                # break
                with open('tweets.json', mode="w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                    return status.HTTP_200_OK
            
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sorry, tweet not found.."
        )