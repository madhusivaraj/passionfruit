from flask import Flask, request, jsonify
import json
from pymongo import MongoClient
from bson import ObjectId
app = Flask(__name__)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

client = MongoClient('localhost', 27017)

user_db = client['user_db']

users = []

@app.route("/users", methods=["POST", "GET"])
def users_list():
    if request.method == 'GET':
        user_coll = user_db['users']
        return JSONEncoder().encode(list(user_coll.find()))
    else:
        user = {
            "username": request.get_json()['username'],
            "name": request.get_json()['name'],
            "age": request.get_json()['age'],
            "major": request.get_json()['major'],
            "year": request.get_json()['year']
        }
        user_coll = user_db['users']
        user_coll.insert_one(user)
        #print user["socials"]["insta"]
        return "Done."

@app.route("/users/<user_name>", methods=["DELETE"])
def user_delete(user_name):
    user_coll = user_db['users']
    user_coll.delete_one({"username": user_name})
    return "Deleted user."

@app.route("/users/<user_name>", methods=["POST"])
def user_update():
    users.remove(user_name)
    users.append(request.get_json()['username'])
    return "Replaced " + username + " with " + request.get_json()['username']

@app.route("/users?majors=<major>", methods=["GET"])
def filter_user_by_major(major):
    user_coll = user_db['users']
    return JSONEncoder().encode(list(user_coll.find({'major': major})))
    #key and value

@app.route("/users/years/<year>", methods=["GET"])
def filter_user_by_year(year):
    user_coll = user_db['users']
    return JSONEncoder().encode(list(user_coll.find({'year': year})))

@app.route("/majors", methods=["GET"])
def list_of_majors():
    with open('majors.txt') as majors_list:
        inputs=[]
        for line in majors_list:
            inputs.append(line.rstrip())
        majors=({"majors":inputs})
        return JSONEncoder().encode(majors)

@app.route("/years", methods=["GET"])
def list_of_years():
    with open('years.txt') as years_list:
        inputs=[]
        for line in years_list:
            inputs.append(line.rstrip())
        years=({"years":inputs})
        return JSONEncoder().encode(years)





