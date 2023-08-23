from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
db = client["mydatabase"]
collection = db["users"]