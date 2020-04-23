from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)
app.secret_key = "secretkey"

mongoDev = PyMongo(app, uri="mongodb://andrey:mongopass@cluster0-shard-00-00-ccvwf.mongodb.net:27017,cluster0-shard-00-01-ccvwf.mongodb.net:27017,cluster0-shard-00-02-ccvwf.mongodb.net:27017/testDev?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
mongoProd = PyMongo(app, uri="mongodb://andrey:mongopass@cluster0-shard-00-00-ccvwf.mongodb.net:27017,cluster0-shard-00-01-ccvwf.mongodb.net:27017,cluster0-shard-00-02-ccvwf.mongodb.net:27017/testProd?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

@app.route('/dev/create', methods=['POST'])
def insert_vers_dev():
    if isinstance(request.json, list) == False:
        _json = request.json
        _author = _json['author']
        _text = _json['text']

        if _author and _text:
            try:
                _id = mongoDev.db.test_collection.insert({
                    'author': _author,
                    'text': _text
                })

                resp = jsonify('Verse added successfully')
                resp.status_code = 200
                return resp
            except: return jsonify('Error on Insert')

    elif isinstance(request.json, list):
        _json = request.json

        try:
            for doc in _json:
                _author = doc['author']
                _text = doc['text']

                if _author and _text:
                    _id = mongoDev.db.test_collection.insert({
                        'author': _author,
                        'text': _text
                    })
            
            resp = jsonify('Verses added successfully')
            resp.status_code = 200
            return resp #str(db_response.inserted_ids)
        except: jsonify('Error on Insert Many: Verify if the data is a JSON Array')

    else: return jsonify('No data received')

@app.route('/dev/list', methods=['GET'])
def list_vers_dev():
    verses = mongoDev.db.test_collection.find()

    resp = dumps(verses)
    return resp

@app.route('/dev/verse/<id>', methods=['GET'])
def select_vers_dev(id):
    verse = mongoDev.db.test_collection.find_one({'_id': ObjectId(id)})

    resp = dumps(verse)
    return resp

@app.route('/dev/delete/<id>', methods=['DELETE'])
def delete_verse_dev(id):
    mongoDev.db.test_collection.delete_one({'_id': ObjectId(id)})

    resp = jsonify('Verse deleted successfully')
    resp.status_code = 200
    return resp

@app.route('/dev/update/<id>', methods=['PUT'])
def update_vers_dev(id):
    _id = id
    _json = request.json
    _author = _json['author']
    _text = _json['text']

    if _author and _text:
        mongoDev.db.test_collection.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'author': _author, 'text': _text}})

        resp = jsonify('Verse updated successfully')
        resp.status_code = 200
        return resp

# ======================================  PROD  ====================================== #

@app.route('/prod/create', methods=['POST'])
def insert_vers():
    if isinstance(request.json, list) == False:
        _json = request.json
        _author = _json['author']
        _text = _json['text']

        if _author and _text:
            try:
                _id = mongoProd.db.test_collection.insert({
                    'author': _author,
                    'text': _text
                })

                resp = jsonify('Verse added successfully')
                resp.status_code = 200
                return resp
            except: return jsonify('Error on Insert')

    elif isinstance(request.json, list):
        _json = request.json

        try:
            for doc in _json:
                _author = doc['author']
                _text = doc['text']

                if _author and _text:
                    _id = mongoProd.db.test_collection.insert({
                        'author': _author,
                        'text': _text
                    })
            
            resp = jsonify('Verses added successfully')
            resp.status_code = 200
            return resp #str(db_response.inserted_ids)
        except: jsonify('Error on Insert Many: Verify if the data is a JSON Array')

    else: return jsonify('No data received')

@app.route('/prod/list', methods=['GET'])
def list_vers():
    verses = mongoProd.db.test_collection.find()

    resp = dumps(verses)
    return resp

@app.route('/prod/verse/<id>', methods=['GET'])
def select_vers(id):
    verse = mongoProd.db.test_collection.find_one({'_id': ObjectId(id)})

    resp = dumps(verse)
    return resp

@app.route('/prod/delete/<id>', methods=['DELETE'])
def delete_verse(id):
    mongoProd.db.test_collection.delete_one({'_id': ObjectId(id)})

    resp = jsonify('Verse deleted successfully')
    resp.status_code = 200
    return resp

@app.route('/prod/update/<id>', methods=['PUT'])
def update_vers(id):
    _id = id
    _json = request.json
    _author = _json['author']
    _text = _json['text']

    if _author and _text:
        mongoProd.db.test_collection.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'author': _author, 'text': _text}})

        resp = jsonify('Verse updated successfully')
        resp.status_code = 200
        return resp

if __name__ == "__main__":
    app.run(debug=True)