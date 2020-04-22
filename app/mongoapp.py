import pymongo
import datetime
from bson.json_util import dumps

def connection():
    try:
        client = pymongo.MongoClient(
            "mongodb://andrey:mongopass@cluster0-shard-00-00-ccvwf.mongodb.net:27017,cluster0-shard-00-01-ccvwf.mongodb.net:27017,cluster0-shard-00-02-ccvwf.mongodb.net:27017/testpy?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    except: print('Database connect error')
    return client

# ------------------- OPERATIONS -------------------
# INSERT
def create_one(coll, data):
    try:
        op = coll.insert_one(data)
        return op
    except: print('Insert operation error')

def create_many(coll, data):
    try:
        op = coll.insert_many(data)
        return op
    except: print('Insert many operation error')

# SELECT
def select(coll, data):
    try:
        op = dumps(coll.find(data))
        return op
    except: print('Find operation error')

def select_all(coll):
    try:
        op = dumps(coll.find())
        return op
    except: print('Find all operation error')

# UPDATE
def update_one(coll, query, data):
    try:
        coll.update_one(query, { '$set': data })
    except: print('Update operation error')

# DELETE 
def delete(coll, query):
    try:
        coll.delete_one(query)
    except: print('Delete operation error')


""" x = register_many(coll, post)
print(x.inserted_ids) """