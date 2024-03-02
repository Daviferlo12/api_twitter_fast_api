#PYTHON
from typing import Optional
from uuid import UUID, uuid4
from uuid import UUID
#MODEL
from db.models.Tweet import Tweet
#PYDANTIC
from pydantic import(
    Field
)

class TweetDB(Tweet):
    tweet_id : Optional[UUID] = Field(default_factory=uuid4, title="UUID version 4")