#MODELS
from models.User import User

#PYDANTIC
from pydantic import(
    Field
)


class UserRegister(User):
    password : str = Field(
        ...,
        min_length=8,
        max_length=64
    )
    class Config:
        exclude = {'user_id'}
    