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
    tweets,users, jwt_authentication, users_db, tweets_db, jwt_autentication_db
)

#MODELS
from db.models.Tweet import Tweet

#ESCHEMAS
from db.schemas.tweet import tweets_schema

#DB
from db.con import db_client


description = """
        Tweeter API simulation. To use some of the endpoint you will have to be autenticated to generete an API TOKEN which will have a durarion of 20 minutes 🚀
        
        You will be able to:

        * **Create users and tweets ** (_not implemented_yet).
        * **Get users (depend on your role) and tweets** (_not implemented_yet).
        * **Update users (depend on your role) and tweets** (_not implemented_yet).
        * **Delete users (depend on your role) and tweets** (_not implemented_yet).
                """

app = FastAPI(
    title = "TWETTER API",
    version = "0.0.1",
    description = description,
    contact={
        "name": "David Lopez",
        "url": "https://www.linkedin.com/in/david-lopez69/",
        "email": "daviferlo12@gmail.com",
    }
)

# INSTANCIES OF ROUTERS
app.include_router(tweets.router)
app.include_router(users.router)

# autentication_routers

# app.include_router(basic_auth.router)
#app.include_router(jwt_authentication.router)
app.include_router(jwt_autentication_db.router)

# users DB
app.include_router(users_db.router)

# users DB
app.include_router(tweets_db.router)

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
    return tweets_schema(db_client.local.tweets.find())