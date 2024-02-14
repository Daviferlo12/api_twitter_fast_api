#PYTHON
from uuid import UUID, uuid4
from typing import List
from passlib.context import CryptContext


# FAST API
from fastapi import(
    status, Body, Path, HTTPException, Depends, APIRouter
)


#MODELS
from db.models.User import User
from db.models.UserDB import UserDB


#LOGIN FUNCTIONS
from routers.jwt_authentication import current_user


#DB
from db.con import db_client

#SCHEMAS
from db.schemas.user import user_schema, users_schema

#passlib instance
pwd_crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users_db",
    tags=["Users"],
    responses={status.HTTP_404_NOT_FOUND: {'Message' : "Error: Not Found.."}}
)


## USERS


### Register User
@router.post(
    path="/sign_up",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User"
)
def signup(user : UserDB = Body(...)):
    
    """
    SignUp a user
    
    This endpoint register a user un the app
    
    Parameter:
    - Request boby parameter
        - User : UserRegister

    Returns a json with the basic information of the user:
    - user_id: UUID
    - email: Emailstr
    - first_name : str
    - last_name : str
    - birth_date: dateTime
    """
    if type(search_user('email',user.email)) == User:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'User already exists'
        )
    
    user_dict = dict(user)
    user_dict["_id"] = uuid4()
    user_dict['password'] = str(pwd_crypt.hash(user_dict["password"]))
    
    #Insert the userRegister Object and get the user's _id
    id = db_client.local.users.insert_one(user_dict).inserted_id
    
    # Get the inserted object using the schema function
    new_user = user_schema(db_client.local.users.find_one({"_id" : id}))
        
    return User(**new_user)   


### Show all users
@router.get(
    path="/",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users"
)
def show_all_users(user : User = Depends(current_user)):
    """
    **Show all Users**

    This endpoint shows all users in the app.

    Parameters:
        -

    Returns a JSON list with all users in the app, with the following structure:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: dateTime
    """
    return users_schema(db_client.local.users.find())


### Show an especific user
@router.get(
    path="/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user"
)
def  show_a_user(user_id : UUID = Path(...), user : User = Depends(current_user)):
    """
    Get a User
    
    This is an endpoint to get an especific user
    
    Parameters:
    - user_id : UUID

    Returns a json with the information of the user:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: dateTime
        
    """
     
    return search_user('_id', user_id)   
    

## Delete a user
@router.delete(
    path="/{user_id}/delete",
    # response_model=User,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a User"
)
def delete_a_user(user_id : UUID = Path(...), user : User = Depends(current_user)):
    """
    Delete a User
    
    This is an endpoint to delete a user
    
    Parameters:
    - user_id : UUID

    Returns a HTTP response 200 if the user was correctly deleted
        
    """
        
    result = db_client.local.users.find_one_and_delete({'_id' : user_id})
    
    if not result:     
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error, user not eliminated"
        )
        

### Update a user
@router.put(
    path="/update",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Update a User"
)
def update_a_user(user : User = Body(...), user_auth : User = Depends(current_user)):
    """
    **Update a User**
    
    This is an endpoint to update an especific user
    
    Body parameter:
    - user : User

    Returns a json with the information of the updated user:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: dateTime
        
    """
        
    user_dict = dict(user)
    user_dict["_id"] = user_dict['user_id']
    del user_dict["user_id"]
    
    try:
        db_client.local.users.find_one_and_replace({'_id' : user.user_id}, user_dict)
    except:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User did not update correctly..."
        )
            
    return search_user('_id', user.user_id)
    


# VALIDATE IF THE EMAIL ALREADY EXISTS ON THE DATA BASE
def search_user(field : str, key): 
    try:
        user = user_schema(db_client.local.users.find_one({field : key}))
        return User(**user)
    except:
        return {'error' : 'User not found'}