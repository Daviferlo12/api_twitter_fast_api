#MODEL
from db.models.UserBase import UserBase

#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    Field, SecretStr
)


class UserLogin(UserBase):
    password : SecretStr = Field(
        ...,
        min_length=8,
        max_length=64
    )
