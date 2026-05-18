import os
from flask import Flask, request, jsonify, session, redirect
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "super_secret_tracker_key"

client = MongoClient(os.environ.get("MONGO_URI"), serverSelectionTimeoutMS=5000)
db = client["tracker"]
employees = db["employees"]
collection = db["logs"]
admin=db["admin"]

@app.route('/log', methods=['POST'])
def log():
    data = request.json
    collection.insert_one(data)
    print("Saved:", data)
    return jsonify({"ok": True})
@app.route('/data', methods=['GET'])
def get_data():
    logs = list(collection.find({}, {"_id": 0}).sort("_id", -1).limit(20))
    return jsonify(logs)

@app.route('/active', methods=['GET'])
def active_users():

    logs = list(
        collection.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(100)
    )

    users = {}

    for log in logs:
        user = log.get("user")

        if user not in users:
            users[user] = log

    return jsonify(list(users.values()))
    
@app.route('/history/<date>', methods=['GET'])
def history(date):

    logs = list(
        collection.find(
            {"date": date},
            {"_id": 0}
        ).sort("timestamp", -1)
    )
    return jsonify(logs)
    
@app.route('/users', methods=['GET'])
def users():
    all_users = collection.distinct("user")
    return jsonify(all_users)

@app.route('/validate-user', methods=['POST'])
def validate_user():

    data = request.json

    employee = employees.find_one({
        "userId": data.get("userId")
    })

    if not employee:
        return jsonify({
            "ok": False,
            "message": "Invalid ID"
        })

    return jsonify({
        "ok": True,
        "name": employee["name"]
    })
    
@app.route('/')
def home():
    return open("dashboard.html").read()

if __name__ == "__main__":
    app.run()
