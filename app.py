from flask import Flask, request, jsonify
import json, uuid
from pymongo import MongoClient
from bson import ObjectId
from functools import wraps
app = Flask(__name__)

import firebase_admin
from firebase_admin import credentials, auth


cred = credentials.Certificate('firebase.json')
default_app = firebase_admin.initialize_app(cred)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

client = MongoClient('mongodb+srv://admin:madhusivaraj@passionfruit-uqm6q.mongodb.net/test?retryWrites=true', 27017)

user_db = client['user_db']

users = []

# This function is a decorator
def auth_required(f):
    @wraps(f)
    def verify_token(*args, **kwargs):
        # Verify firebase auth token here
        try:    
            id_token = request.args.get('token')
            t = auth.get_user(id_token)
            print(t.toJSON())
            custom_token=auth.create_custom_token(id_token)
            result = auth.verify_id_token(custom_token)
            print(result['name'] + " made a request")
        except Exception as e:
            print(e)
            return jsonify({"error": "Bad token"})      
        return f(*args, **kwargs)
    return verify_token

@app.route("/")
def hello():
    return "PASSIONFRUIT"

@app.route("/login")
def login():
    return "login"

@app.route("/users", methods=["POST"])
#@auth_required
def users_list():
        user_id = str(uuid.uuid4());
        user = {
            "user_id": user_id,
            "username": request.get_json()['username'],
            "name": request.get_json()['name'],
            "age": request.get_json()['age'],
            "major": request.get_json()['major'],
            "year": request.get_json()['year']
        }
        user_coll = user_db['users']
        user_coll.insert_one(user)
        #print user["socials"]["insta"]
        return "Created user."

@app.route("/users", methods=["DELETE"])
#@auth_required
def user_delete():
    user_id = request.args.get('user_id')
    user_coll = user_db['users']
    user_coll.delete_one({"user_id": user_id})
    return "Deleted user."

@app.route("/users", methods=["POST"])
#@auth_required
def user_update():
    user_id = request.args.get('user_id')
    user_coll = user_db['users']
    user_coll.update_one({"user_id": user_id})
    return "Update user."

@app.route("/users", methods=["GET"])
#@auth_required
def filter_by():
    user_coll = user_db['users']
    #print(request.args)
    return JSONEncoder().encode(list(user_coll.find(request.args)))

@app.route("/majors", methods=["GET"])
#@auth_required
def list_of_majors():
    with open('majors.txt') as majors_list:
        inputs=[]
        for line in majors_list:
            inputs.append(line.rstrip())
        majors=({"majors":inputs})
        return JSONEncoder().encode(majors)

@app.route("/years", methods=["GET"])
#@auth_required
def list_of_years():
    with open('years.txt') as years_list:
        inputs=[]
        for line in years_list:
            inputs.append(line.rstrip())
        years=({"years":inputs})
        return JSONEncoder().encode(years)

