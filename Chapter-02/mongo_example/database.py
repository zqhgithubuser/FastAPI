from pymongo import MongoClient

client = MongoClient("mongodb://172.16.0.100:27017")

database = client.mydatabase

user_collection = database["users"]
