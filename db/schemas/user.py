def user_schema(user) -> dict:
    return {
        "user_id" : str(user['_id']),
        "email" : user['email'],
        "username" : user['username'],
        "first_name" : user['first_name'],
        "last_name" : user['last_name'],
        "birth_date" : user['birth_date']
    }
    
    
def user_schema_DB(user) -> dict:
    return {
        "user_id" : str(user['_id']),
        "username" : user['username'],
        "email" : user['email'],
        "first_name" : user['first_name'],
        "last_name" : user['last_name'],
        "birth_date" : user['birth_date'],
        "desable" : user['desable'],
        "password" : user['password']
    }


def users_schema(users) -> list:
    return [user_schema(user) for user in users]