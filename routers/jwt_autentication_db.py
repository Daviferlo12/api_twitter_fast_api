# FAST API
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# PYTHON
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from datetime import datetime, timedelta

#SCHEMAS
from db.schemas.user import user_schema
#from db.schemas.user import user_schema_DB

#DB
from db.con import db_client
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

#MODELS
from db.models.User import User
from db.models.UserDB import UserDB

ALGORITHM = "HS256"

acces_token_duration = 20
secret = "0b69c4486093953c50403bd4c7c2ba3b1007c630059f6783700bd946bf1bed32"

router = APIRouter()


oauth2 = OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def search_user_db(field : str, key):
    try:
        user = db_client.local.users.find_one({field : key})

        if user is not None:
            return UserDB(**user)
        else:
            return {'Error' : 'User nor found'}     
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        return {'error': f'MongoDB error: {e}'}
    
    except Exception as e:
        return {'error': f'Unexpected error: {e}'}
    
    
def search_user(field : str, key): 
    try:
        user = user_schema(db_client.local.users.find_one({field : key}))
        return User(**user)
    except:
        return {'error' : 'User not found'}
   


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
    
    return search_user('username', username)

    
async def current_user(user : User = Depends(auth_user)):
    
    if user.desable:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "ERROR: user disabled..."
        )
    
    return user 

    
@router.post(path='/login')
async def login(form : OAuth2PasswordRequestForm = Depends()):
    
    #Validate is the user exists
    user = search_user('username', form.username)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "ERROR: User not found.."
        )
        
    #Validate the user's password
    user_db = search_user_db('username', form.username)
    if not crypt.verify(form.password, user_db.password):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "ERROR: Invalid password.."
        )
        
    acces_token = {
        "sub" : str(user.username),
        "exp" : datetime.utcnow() + timedelta(minutes=acces_token_duration)
    }
        
    return {'access_token' : jwt.encode(acces_token, secret, algorithm = ALGORITHM), 'token_type': 'bearer'}



@router.get(path="/users/me")
async def me(user : User = Depends(current_user)):
    return user

