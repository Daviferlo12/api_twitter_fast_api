#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    EmailStr, Field
)

class UserBase(BaseModel):
    user_id : str = Field(...)
    email : EmailStr = Field(...)