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
    tweets,users, jwt_authentication, users_db, tweets_db
)

#MODELS
from models.Tweet import Tweet
from models.User import User


app = FastAPI()
app.title = "TWETTER API"
app.version = "0.0.1"
app.description = """API para la creacion, lectura, actualizacion y eliminacion de tweets y usuarios \n
                    Para poder usar consumir ciertos enpoints debes estar autenticado, primero con el fin de generar un token que tiene una duracion de 20 minutos.\n
                    Finalmente para consumir estos enpoint necesitaras enviar el token con tu request."""

# INSTANCIES OF ROUTERS
app.include_router(tweets.router)
app.include_router(users.router)

# autentication_routers
# app.include_router(basic_auth.router)
app.include_router(jwt_authentication.router)

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
    
    with open("tweets.json", mode="r", encoding="utf-8") as file:
        results = json.loads(file.read())
        return results