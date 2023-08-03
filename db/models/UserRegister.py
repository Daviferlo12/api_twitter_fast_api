#MODELS
from db.models.user import User

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
        exclude = {'desable'}