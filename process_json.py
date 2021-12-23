import json
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
load_dotenv()

uri = getenv('uri')

client = MongoClient(uri)
db = client.get_database("ratings")
collection = db.get_collection("anime")

d = {}
with open('imdb.json') as json_file:
    d = json.load(json_file)

def find_by_id(id):
    cursor = collection.find({"_id":id})
    return cursor

def update_array(id):
    cursor = collection.update({'_id':'all_anime'}, {'$addToSet':{"arr":id}})

def process_dict(dictionary):
    for title in dictionary:
        update_array(title)
        result = find_by_id(title)
        arr = dictionary[title]
        if result.count() == 0:
            post = {"_id": title, "rating":arr[0], "description":arr[1], "image":arr[2]}
            collection.insert_one(post)
        else:
            new_val = {"$set": {"rating":arr[0], "description":arr[1], "image":arr[2]}}
            collection.update_one({"_id":title},new_val)

process_dict(d)
