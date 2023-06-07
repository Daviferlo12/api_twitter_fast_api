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

app = FastAPI()

@app.get(path="/")
def home():
    return {"Twitter API": "Working.."}

## USERS

@app.post(
    path="/signUp",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def  signup():
    pass


@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="login a user",
    tags=["Users"]
)
def login():
    pass


@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def  show_all_users():
    pass


@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
)
def  show_a_user():
    pass


@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user():
    pass


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
