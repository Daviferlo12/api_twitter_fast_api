#PYTHON
from uuid import UUID
from typing import List
import json

# FAST API
from fastapi import(
    status, Body, Path, HTTPException, Depends, APIRouter
)

#MODELS
from models.User import User
from models.UserLogin import UserLogin
from models.UserBase import UserBase
from models.UserRegister import UserRegister

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {'Message' : "Error: Not Found.."}}
)

#LOGIN FUNCTIONS
from routers.jwt_authentication import current_user

## USERS

### Register User
@router.post(
    path="/signUp",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User"
)
def  signup(user : UserRegister = Body(...)):
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
    with open(file="users.json", mode="r+", encoding="utf-8") as file:
        results = json.loads(file.read())
        
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birth_date'] = str(user_dict['birth_date'])
        results.append(user_dict)
        file.seek(0)
        file.write(json.dumps(results))     
        
        return user   


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
    
    with open("users.json", mode="r", encoding="utf-8") as file:
        results = json.loads(file.read())
        return results

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
    with open("users.json", mode="r", encoding="utf-8") as file:
        result = json.loads(file.read())
        
        for user in result:
            if user['user_id'] == str(user_id):             
                return user
                
                
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "This user does not exist"
        )

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

