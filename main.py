#PYTHON
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    EmailStr, Field
)
# FAST API
from fastapi import FastAPI
from fastapi import(
    status
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
def  signup():
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
        - birth_date: str
    """
    pass

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
def  show_all_users():
    pass

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
def post():
    pass


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