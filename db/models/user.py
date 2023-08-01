#PYTHON
from datetime import date
from typing import Optional

#MODEL
from db.models.UserBase import UserBase

#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    Field
)

class User(UserBase):
    first_name : str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name : str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date : Optional[date] = Field(default=None)
    