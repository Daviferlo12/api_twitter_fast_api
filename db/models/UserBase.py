#PYTHON
from uuid import UUID
from typing import Optional

#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    EmailStr, Field
)



class UserBase(BaseModel):
    user_id : Optional[str] = Field()
    email : EmailStr = Field(...)
    desable : bool = Field(default=False)