# FAST API
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# PYTHON
from pydantic import BaseModel
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"

acces_token_duration = 2
secret = "0b69c4486093953c50403bd4c7c2ba3b1007c630059f6783700bd946bf1bed32"

router = APIRouter()


oauth2 = OAuth2PasswordBearer(tokenUrl='login')

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
        'password' : '$2a$12$OksUPjFTZLVwyUD8HaGNxO2j2iTZrGqi9a4PiopreVPdK2iQQ3Ffy'
     },
    "daviferlo12" : {
        'username' : 'daviferlo12',
        'full_name' : 'David Lopez 2',
        'email' : 'daviferlo@gmail.com',
        'disable' : True,
        'password' : '$2a$12$bOnZGaUXc2yQT9q5N9zBmOlgH2dttDS/6QaKV7Ue6HmF5i9UG1GO6'
     }
}

def search_user_db(username : str):
    if username in users_db:
        return User_DB(**users_db[username])
    
def search_user(username : str):
    if username in users_db:
        return User(**users_db[username])
   


async def auth_user(token : str = Depends(oauth2)):
    
    exeption = HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "ERROR: invalid credentials...",
                headers={"WWW-Authenticate" : "Bearer"}
            )
    try: 
        username = jwt.decode(token, secret, algorithms = [ALGORITHM]).get("sub")
        if username is None:
            raise exeption
    except ExpiredSignatureError:
        raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "Token has expired...",
                headers={"WWW-Authenticate" : "Bearer"}
            )
    except JWTError:
        raise exeption
    
    return search_user(username)


    
async def current_user(user : User = Depends(auth_user)):
        
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
        "exp" : datetime.utcnow() + timedelta(minutes=acces_token_duration)
    }
        
    return {'access_token' : jwt.encode(acces_token, secret, algorithm = ALGORITHM), 'token_type': 'bearer'}



@router.get(path="/users/me")
async def me(user : User = Depends(current_user)):
    return user

