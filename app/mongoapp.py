import pymongo as pm
from bson.json_util import dumps

def connection():
    try:
        client = pm.MongoClient(
            "mongodb://andrey:mongopass@cluster0-shard-00-00-ccvwf.mongodb.net:27017,cluster0-shard-00-01-ccvwf.mongodb.net:27017,cluster0-shard-00-02-ccvwf.mongodb.net:27017/testpy?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    except: print('Database connect error')
    return client

# ------------------- OPERATIONS -------------------
# INSERT
def create_one(coll, data):
    op = coll.insert_one(data)
    return op

def create_many(coll, data):
    op = coll.insert_many(data)
    for x in op:
        print(x)
    return op.inserted_ids

# SELECT
def select(coll, data):
    op = dumps(coll.find(data))
    return op

def select_all(coll):
    op = dumps(coll.find())
    return op

# UPDATE
def update_one(coll, query, data):
    coll.update_one(query, { '$set': data })

# DELETE 
def delete(coll, query):
    coll.delete_one(query)


""" x = register_many(coll, post)
print(x.inserted_ids) """