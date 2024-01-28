#PYTHON
from datetime import date
from typing import Optional

#PYDANTIC
from pydantic import(
    Field, BaseModel, EmailStr
)

class User(BaseModel):
    username : str = Field(...)
    email : EmailStr = Field(...)
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
    birth_date : Optional[str] = Field(default= date.today())
    desable : bool = Field(default=False)
    