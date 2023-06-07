#PYTHON
from uuid import UUID

#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    EmailStr, Field
)



class UserBase(BaseModel):
    user_id : UUID = Field(...)
    email : EmailStr = Field(...)