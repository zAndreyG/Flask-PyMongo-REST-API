from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.json_util import dumps
from bson.objectid import ObjectId
import mongoapp as mongoapp

app = Flask(__name__)
CORS(app)
app.secret_key = "secretkey"
app.config['MONGO_URI'] = "mongodb://andrey:mongopass@cluster0-shard-00-00-ccvwf.mongodb.net:27017,cluster0-shard-00-01-ccvwf.mongodb.net:27017,cluster0-shard-00-02-ccvwf.mongodb.net:27017/testpy?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"

mongo = PyMongo(app)

@app.route('/create', methods=['POST'])
def insert_vers():
    if isinstance(request.json, list) == False:
        _json = request.json
        _author = _json['autor']
        _text = _json['texto']

        if _author and _text:
            try:
                _id = mongo.db.test_collection.insert({
                    'autor': _author,
                    'texto': _text
                })

                resp = jsonify('Verse added successfully')
                resp.status_code = 200
                return resp
            except: return jsonify('Bad Request')

    else: return jsonify('No data')

    """ elif isinstance(request.json, list):
        client = mongoapp.connection()
        coll = client["test_collection"]
    
        try:
            _ids = mongoapp.create_many(coll, request.json)

            resp = jsonify('Verses added successfully')
            resp.status_code = 200
            return resp #str(db_response.inserted_ids)

        except: return jsonify('Bad Request: Verify if the data is a JSON Array') """

@app.route('/list', methods=['GET'])
def list_vers():
    verses = mongo.db.test_collection.find()

    resp = dumps(verses)
    return resp

@app.route('/verse/<id>', methods=['GET'])
def select_vers(id):
    verse = mongo.db.test_collection.find_one({'_id': ObjectId(id)})

    resp = dumps(verse)
    return resp

@app.route('/delete/<id>', methods=['DELETE'])
def delete_verse(id):
    mongo.db.test_collection.delete_one({'_id': ObjectId(id)})

    resp = jsonify('User deleted successfully')
    resp.status_code = 200
    return resp

@app.route('/update/<id>', methods=['PUT'])
def update_vers(id):
    _id = id
    _json = request.json
    _author = _json['autor']
    _text = _json['texto']

    if _author and _text:
        mongo.db.test_collection.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'autor': _author, 'texto': _text}})

        resp = jsonify('Verse updated successfully')
        resp.status_code = 200
        return resp

if __name__ == "__main__":
    app.run(debug=True)