#PYTHON
from typing import Optional
from uuid import UUID, uuid4

# CLASS FATHER
from db.models.User import User

#PYDANTIC
from pydantic import(
    Field
)

class UserDB(User):
    user_id : Optional[UUID] = Field(default_factory=uuid4, title="UUID version 4")