import json



user_id = '3fa85f64-5717-4562-b3fc-2c963f66afa6'

with open("users.json", mode="r", encoding="utf-8") as file:
    result = json.loads(file.read())
    
    for user in result:
        if user['user_id'] == str(user_id):             
            print(result[result.index(user)])
            
        


