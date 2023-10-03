from pymongo import MongoClient


# DB LOCALHOST
db_client = MongoClient("localhost", 27017, uuidRepresentation='standard')

# DB REMOTE
#db_client = MongoClient(
#    "mongodb+srv://daviferlob12:TmwSYKw5CRR5TUVY@cluster0.64wvdt1.mongodb.net/?retryWrites=true&w=majority",
#    uuidRepresentation='standard').test