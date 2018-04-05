import json
from pymongo import MongoClient
import pprint
import bson

client = MongoClient()
db = client.get.database
collection = db.get_collection

posts = db.posts

with open('labels.json') as json_file: 
	info = json.load(json_file)
	posts.insert_one(info)
