#PYTHON
from typing import Optional

#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    EmailStr, Field
)

class UserBase(BaseModel):
    email : EmailStr = Field(...)
    desable : bool = Field(default=False)