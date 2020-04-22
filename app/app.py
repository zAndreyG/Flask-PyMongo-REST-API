from flask import Flask, request
from flask_cors import CORS
import pymongo
import mongoapp as mongoapp

app = Flask(__name__)
CORS(app)

@app.route('/vers/create', methods=['POST'])
def insert_vers():
    client = mongoapp.connection()
    db = client["testpy"]
    coll = db["test_collection"]

    if request.json:
        try:
            if len(request.json) == 1:
                db_response = mongoapp.create_one(coll, request.json[0])
                return str(db_response.inserted_id)

            elif len(request.json) > 1:
                db_response = mongoapp.create_many(coll, request.json)
                return str(db_response.inserted_ids)

        except: return 'Bad Request: The data must be a JSON Array'
    else: return "No data"

@app.route('/vers/list', methods=['GET'])
def select_vers():
    client = mongoapp.connection()
    db = client["testpy"]
    coll = db["test_collection"]

    db_response = mongoapp.select_all(coll)
    return str(db_response)

@app.route('/vers/update', methods=['POST'])
def update_vers():
    client = mongoapp.connection()
    db = client["testpy"]
    coll = db["test_collection"]

    if request.json:
        try:
            mongoapp.update_one(coll, request.json[0], request.json[1])
            return 'OK'
        except: return 'Bad Request: The data must be a JSON Array --> [query, modifications]'


if __name__ == "__main__":
    app.run(debug=True)