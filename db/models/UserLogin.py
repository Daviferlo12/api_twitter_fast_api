#MODEL
from db.models.UserDB import UserDB

#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    Field, SecretStr
)


class UserLogin(UserDB):
    password : str = Field(
        ...,
        min_length=8,
        max_length=64
    )
