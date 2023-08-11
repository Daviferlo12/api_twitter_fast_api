#PYTHON
from uuid import UUID
from typing import List
import json
from datetime import date
from bson import Binary


# FAST API
from fastapi import(
    status, Body, Path, HTTPException, Depends, APIRouter
)


#MODELS
from db.models.user import User
from db.models.UserLogin import UserLogin
from db.models.UserBase import UserBase
from db.models.UserRegister import UserRegister


#LOGIN FUNCTIONS
from routers.jwt_authentication import current_user


#DB FUNCTIONS
from db.user import db_client

#SCHEMAS
from db.schemas.user import user_register_schema


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
def signup(user : UserRegister = Body(...)):
    
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
    if type(search_user_by_email(user.email)) == User:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'User already exists'
        )
    
    user_dict = dict(user)
    user_dict["_id"] = user_dict['user_id']
    del user_dict["user_id"]
    
    #Insert the userRegister Object
    id = db_client.local.users.insert_one(user_dict).inserted_id
    
    # Get the inserted object using schema
    new_user = user_register_schema(db_client.local.users.find_one({"_id" : id}))
        
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

    return [user_register_schema(us) for us in db_client.local.users.find()]


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
    # Get the user object using schema
    get_user = user_register_schema(db_client.local.users.find_one({"_id" : user_id}))
        
    return User(**get_user)   
    

## Delete a user
@router.delete(
    path="/{user_id}/delete",
    # response_model=User,
    status_code=status.HTTP_200_OK,
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
    with open('users.json', mode="r+", encoding="utf-8") as file:
        
        results = json.loads(file.read())
        
        for user in results:
            if user['user_id'] == str(user_id):
                results.remove(user)
                # break
                with open('users.json', mode="w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                    return status.HTTP_200_OK
            
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sorry, User no found.."
        )

### Update a user
@router.put(
    path="/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User"
)
def update_a_user(user_id : UUID = Path(...), user : User = Body(...), user_auth : User = Depends(current_user)):
    """
    **Update a User**
    
    This is an endpoint to update an especific user
    
    Path Parameter:
    - user_id : UUID
    
    Body parameter:
    - user : User

    Returns a json with the information of the updated user:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: dateTime
        
    """
    with open('users.json', mode="r+", encoding="utf-8") as file:
        
        results = json.loads(file.read())
        
        user_dict = user.dict()
        user_dict['user_id'] = str(user.user_id)
        user_dict['email'] = user.email
        user_dict['first_name'] = user.first_name
        user_dict['last_name'] = user.last_name
        user_dict['birth_date'] = str(user.birth_date)

        for user in results:
            if user['user_id'] == str(user_id):
                
                results[results.index(user)] = user_dict
                
                # break
                with open('users.json', mode="w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(results))
                    return user
            
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sorry, User no found.."
        )


# VALIDATE IF THE EMAIL ALREADY EXISTS ON THE DATA BASE

def search_user_by_email(email : str): 
    try:
        user = user_register_schema(db_client.local.users.find_one({'email' : email}))
        return User(**user)
    except:
        return {'error' : 'User not found'}