from pymongo import MongoClient


mongodb_uri = "mongodb+srv://Emna:11128766@cluster0.9mzij.mongodb.net/test"
port = 8000
connection = MongoClient(mongodb_uri, port)

# Users collection located in sig database
users_collection = connection.sig.users
admins_collection = connection.sig.admins
