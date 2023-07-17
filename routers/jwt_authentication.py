# FAST API
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


algorithm = "HS256"

acces_token_duration = 1

app = FastAPI()


oauth2 = OAuth2PasswordBearer(tokenUrl='Login')

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username : str
    full_name : str
    email : str
    disable : bool
    
class User_DB(User):
    password : str
    
users_db = {
     "daviferlo" : {
        'username' : 'daviferlo',
        'full_name' : 'David Lopez',
        'email' : 'daviferlo@gmail.com',
        'disable' : False,
        'password' : '$2a$12$c5X0dKFEZQQTs82NvhO3I.tLL3wdGvWfE4fpKdIfgezHkV.PuXpVS'
     },
    "daviferlo12" : {
        'username' : 'daviferlo12',
        'full_name' : 'David Lopez 2',
        'email' : 'daviferlo@gmail.com',
        'disable' : True,
        'password' : '$2a$12$vJUvSW8FhblMzy2zkMmm4.dyqwCwcnSmbwEOGGhjxslaKcv5ZCUaq'
     }
}

def search_user_db(username : str):
    if username in users_db:
        return User_DB(**users_db[username])
    
    
@app.post(path='/login')
async def login(form : OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "ERROR: User not found.."
        )
        
    user = search_user_db(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "ERROR: Invalid password.."
        )
        
    acces_token = {
        "sub" : user.username,
        "exp" : datetime.now() + timedelta(minutes=acces_token_duration)
    }
        
    return {'access_token' : acces_token, 'token_type': 'bearer'}

