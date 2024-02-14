from db.con import db_client
from pprint import pprint
from db.models.UserDB import UserDB
from db.schemas.user import user_schema_DB
from routers.jwt_autentication_db import search_user_db

result = search_user_db("username",'daviferlo')

pprint(result)