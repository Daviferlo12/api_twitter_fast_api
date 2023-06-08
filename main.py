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
    status, Body
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
def  show_a_user():
    pass

## Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user():
    pass

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user():
    pass



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
    return {"Twitter API": "Working.."}


### Get a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Get a tweet",
    tags=["Tweets"]
)
def show_tweet():
    pass


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
def update_a_tweet():
    pass


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