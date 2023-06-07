#PYTHON
from uuid import UUID
from datetime import date, datetime
from typing import Optional
#PYDANTIC
from pydantic import BaseModel
from pydantic import(
    EmailStr, Field
)
# FAST API
from fastapi import FastAPI
#MODELS
from models import User, UserLogin, UserBase
from models import Tweet
app = FastAPI()

@app.get(path="/")
def home():
    return {"Twitter API": "Working.."}