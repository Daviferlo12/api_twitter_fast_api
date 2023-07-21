# FAST API
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

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
        'password' : '1234admin'
     },
    "daviferlo12" : {
        'username' : 'daviferlo12',
        'full_name' : 'David Lopez 2',
        'email' : 'daviferlo@gmail.com',
        'disable' : True,
        'password' : '123445rer'
     }
}

def search_user_db(username : str):
    if username in users_db:
        return User_DB(**users_db[username])
    
    
def search_user(username : str):
    if username in users_db:
        return User(**users_db[username])
    
    
async def current_user(token : str = Depends(oauth2)):
    user =  search_user(token)
    
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "ERROR: invalid credentials...",
            headers={'www-Authenticate' : 'Bearer'}
        )
        
    if user.disable:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "ERROR: user disabled..."
        )
    
    return user
    

@router.post(path='/login')
async def login(form : OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "ERROR: user not found..."
        )
        
    user = search_user_db(form.username)
    
    if not form.password == user.password:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "ERROR: invalid password..."
        )
    return {'access_token' : form.username, 'token_type': 'bearer'}


@router.get(path="/users/me")
async def me(user : User = Depends(current_user)):
    return user