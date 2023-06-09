#PYTHON
import json
from typing import List

# FAST API
from fastapi import FastAPI
from fastapi import(
    status
)
from fastapi.staticfiles import StaticFiles

#ROUTERS
from routers import(
    tweets,users
)

#MODELS
from models.Tweet import Tweet
from models.User import User


app = FastAPI()

# INSTANCIES OF ROUTERS
app.include_router(tweets.router)
app.include_router(users.router)

# STATIC RESOURCES
app.mount('/static', StaticFiles(directory='static'), name="static")


### Get all tweets by default
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


### Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="login a user",
    tags=["Users"],
    deprecated=True
)
def login():
    pass