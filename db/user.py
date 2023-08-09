from pymongo import MongoClient

db_client = MongoClient("localhost", 27017, uuidRepresentation='standard')