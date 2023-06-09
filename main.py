#PYTHON
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
import json

#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    EmailStr, Field
)
# FAST API
from fastapi import FastAPI
from fastapi import(
    status, Body, Path, HTTPException
)

#MODELS
from models.User import User
from models.UserLogin import UserLogin
from models.UserBase import UserBase
from models.Tweet import Tweet
from models.UserRegister import UserRegister

app = FastAPI()

## USERS

### Register User
@app.post(
    path="/signUp",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def  signup(user : UserRegister = Body(...)):
    """
    SignUp a user
    
    This endpoint register a user un the app
    
    Parameter:
    - Request boby parameter
        - User : UserRegister

    Returns a json with the basic information of the user:
    - user_id: UUID
    - email: Emailstr
    - first_name : str
    - last_name : str
    - birth_date: dateTime
    """
    with open(file="users.json", mode="r+", encoding="utf-8") as file:
        results = json.loads(file.read())
        
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birth_date'] = str(user_dict['birth_date'])
        results.append(user_dict)
        file.seek(0)
        file.write(json.dumps(results))     
        
        return user   

### Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="login a user",
    tags=["Users"]
)
def login():
    pass

### Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    **Show all Users**

    This endpoint shows all users in the app.

    Parameters:
        -

    Returns a JSON list with all users in the app, with the following structure:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: dateTime
    """
    
    with open("users.json", mode="r", encoding="utf-8") as file:
        results = json.loads(file.read())
        return results

### Show an especific user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
)
def  show_a_user(user_id : UUID = Path(...)):
    """
    Get a User
    
    This is an endpoint to get an especific user
    
    Parameters:
    - user_id : UUID

    Returns a json with the information of the user:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: dateTime
        
    """
    with open("users.json", mode="r", encoding="utf-8") as file:
        result = json.loads(file.read())
        
        for user in result:
            if user['user_id'] == str(user_id):             
                return user
                
                
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "This user does not exist"
        )

## Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    # response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user(user_id : UUID = Path(...)):
    """
    Delete a User
    
    This is an endpoint to delete a user
    
    Parameters:
    - user_id : UUID

    Returns a HTTP response 200 if the user was correctly deleted
        
    """
    with open('users.json', mode="r+", encoding="utf-8") as file:
        
        results = json.loads(file.read())
        
        for user in results:
            if user['user_id'] == str(user_id):
                results.remove(user)
                # break
                with open('users.json', mode="w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                    return status.HTTP_200_OK
            
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sorry, User no found.."
        )

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user(user_id : UUID = Path(...), user : User = Body(...)):
    """
    **Update a User**
    
    This is an endpoint to update an especific user
    
    Path Parameter:
    - user_id : UUID
    
    Body parameter:
    - user : User

    Returns a json with the information of the updated user:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: dateTime
        
    """
    with open('users.json', mode="r+", encoding="utf-8") as file:
        
        results = json.loads(file.read())
        
        user_dict = user.dict()
        user_dict['user_id'] = str(user.user_id)
        user_dict['email'] = user.email
        user_dict['first_name'] = user.first_name
        user_dict['last_name'] = user.last_name
        user_dict['birth_date'] = str(user.birth_date)

        for user in results:
            if user['user_id'] == str(user_id):
                
                results[results.index(user)] = user_dict
                
                # break
                with open('users.json', mode="w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                    return user
            
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sorry, User no found.."
        )



## TWEETS

### Get all tweet by default
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Get all tweets",
    tags=["Tweets"]
    )
def home():
    """
    **Show all tweets**

    This endpoint shows all tweets published in the app.

    Parameters:
        -

    Returns a JSON list with all users in the app, with the following structure:
    - tweet_id: UUID
    - content: str
    - created_at : datetime
    - updated_at : Optional[datetime]
    - by: User
    """
    
    with open("tweets.json", mode="r", encoding="utf-8") as file:
        results = json.loads(file.read())
        return results


### Get a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Get a tweet",
    tags=["Tweets"]
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
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Create a tweet",
    tags=["Tweets"]
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
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary= "Update a tweet",
    tags=["Tweets"]
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
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary= "Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass