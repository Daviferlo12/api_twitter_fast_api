#MODELS
from db.models.User import User

#PYDANTIC
from pydantic import(
    Field, SecretStr
)

class UserRegister(User):
    
    password : str = Field(
        ...,
        min_length=8,
        max_length=64
    )