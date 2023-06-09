#MODEL
from models.UserBase import UserBase

#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    Field
)


class UserLogin(UserBase):
    password : str = Field(
        ...,
        min_length=8,
        max_length=64
    ),
    desible : bool = Field(...)
