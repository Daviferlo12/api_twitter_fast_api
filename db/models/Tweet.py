#PYTHON
from datetime import datetime
from typing import Optional
from uuid import UUID
#MODEL
from db.models.User import User
#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    Field
)

class Tweet(BaseModel):
    content : str = Field(
        ...,
        min_length=1
        ,max_length=256
        )
    created_at : str = Field(default=datetime.now())
    updated_at : Optional[datetime] = Field(default=None)
    by: User = Field(...)