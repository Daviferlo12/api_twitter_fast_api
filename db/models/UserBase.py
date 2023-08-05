#PYTHON
from typing import Optional
from uuid import UUID

#PYDANTIC
from pydantic import(
    EmailStr, Field, BaseModel
)

class UserBase(BaseModel):
    user_id : UUID = Field(...)
    email : EmailStr = Field(...)
    desable : bool = Field(default=False)