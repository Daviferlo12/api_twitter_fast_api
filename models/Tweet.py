#PYTHON
from datetime import datetime
from typing import Optional
from uuid import UUID
#MODEL
import User
#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    EmailStr, Field
)

class Tweet(BaseModel):
    tweet_id : UUID = Field(...)
    content : str = Field(
        ...,
        min_length=1
        ,max_length=256
        )
    created__at : datetime = Field(default=datetime.now())
    updated_at : Optional[datetime] = Field(default=None)
    by: User = Field(...)