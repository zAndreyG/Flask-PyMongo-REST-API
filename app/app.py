from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS  #For Windows
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)  #For Windows
app.secret_key = "secretkey"

mongoDev = PyMongo(app, uri="mongodb://andrey:mongopass@cluster0-shard-00-00-ccvwf.mongodb.net:27017,cluster0-shard-00-01-ccvwf.mongodb.net:27017,cluster0-shard-00-02-ccvwf.mongodb.net:27017/bdDev?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
mongoProd = PyMongo(app, uri="mongodb://andrey:mongopass@cluster0-shard-00-00-ccvwf.mongodb.net:27017,cluster0-shard-00-01-ccvwf.mongodb.net:27017,cluster0-shard-00-02-ccvwf.mongodb.net:27017/bdProd?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")

# ======================================  DEV  ====================================== #

@app.route('/dev/create', methods=['POST'])
def insert_dev():
    if isinstance(request.json, list) == False:
        _json = request.json
        _author = _json['author']
        _text = _json['text']

        if _author and _text:
            try:
                _id = mongoDev.db.quotes.insert_one({
                    'author': _author,
                    'text': _text
                })

                resp = jsonify(
                    _id = str(_id.inserted_id),
                    success = 'Quote added successfully'
                )
                resp.status_code = 200
                return resp
            except: return jsonify(Error = 'Verify the data content')

    elif isinstance(request.json, list):
        idList = []
        _json = request.json

        try:
            _ids = mongoDev.db.quotes.insert_many(_json)

            for _id in _ids.inserted_ids:
                idList.append(str(_id))
            
            resp = jsonify(
                _ids = idList,
                success = 'Quotes added successfully'
            )
            resp.status_code = 200
            return resp
        except: return jsonify(Error = 'Verify the data content')
        

    else: return jsonify(Error = 'No data received')

@app.route('/dev/list', methods=['GET'])
def list_dev():
    quotes = mongoDev.db.quotes.find()

    resp = dumps(quotes)
    return resp

@app.route('/dev/quote/<id>', methods=['GET'])
def select_dev(id):
    quote = mongoDev.db.quotes.find_one({'_id': ObjectId(id)})

    resp = dumps(quote)
    return resp

@app.route('/dev/delete/<id>', methods=['DELETE'])
def delete_dev(id):
    mongoDev.db.quotes.delete_one({'_id': ObjectId(id)})

    resp = jsonify('Quote deleted successfully')
    resp.status_code = 200
    return resp

@app.route('/dev/update/<id>', methods=['PUT'])
def update_dev(id):
    _id = id
    _json = request.json
    _author = _json['author']
    _text = _json['text']

    if _author and _text:
        mongoDev.db.quotes.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'author': _author, 'text': _text}})

        resp = jsonify('Quote updated successfully')
        resp.status_code = 200
        return resp

# ======================================  PROD  ====================================== #

@app.route('/prod/create', methods=['POST'])
def insert_prod():
    if isinstance(request.json, list) == False:
        _json = request.json
        _author = _json['author']
        _text = _json['text']

        if _author and _text:
            try:
                _id = mongoProd.db.quotes.insert_one({
                    'author': _author,
                    'text': _text
                })

                resp = jsonify(
                    _id = str(_id.inserted_id),
                    success = 'Quote added successfully'
                )
                resp.status_code = 200
                return resp
            except: return jsonify(Error = 'Verify the data content')

    elif isinstance(request.json, list):
        idList = []
        _json = request.json

        try:
            _ids = mongoProd.db.quotes.insert_many(_json)

            for _id in _ids.inserted_ids:
                idList.append(str(_id))
            
            resp = jsonify(
                _ids = idList,
                success = 'Quotes added successfully'
            )
            resp.status_code = 200
            return resp
        except: return jsonify(Error = 'Verify the data content')
        

    else: return jsonify(Error = 'No data received')

@app.route('/prod/list', methods=['GET'])
def list_prod():
    quotes = mongoProd.db.quotes.find()

    resp = dumps(quotes)
    return resp

@app.route('/prod/quote/<id>', methods=['GET'])
def select_prod(id):
    quote = mongoProd.db.quotes.find_one({'_id': ObjectId(id)})

    resp = dumps(quote)
    return resp

@app.route('/prod/delete/<id>', methods=['DELETE'])
def delete_prod(id):
    mongoProd.db.quotes.delete_one({'_id': ObjectId(id)})

    resp = jsonify('Quote deleted successfully')
    resp.status_code = 200
    return resp

@app.route('/prod/update/<id>', methods=['PUT'])
def update_prod(id):
    _id = id
    _json = request.json
    _author = _json['author']
    _text = _json['text']

    if _author and _text:
        mongoProd.db.quotes.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'author': _author, 'text': _text}})

        resp = jsonify('Quote updated successfully')
        resp.status_code = 200
        return resp

if __name__ == "__main__":
    app.run(debug=True)