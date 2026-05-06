import os
from flask import Flask, request, jsonify
from pymongo import MongoClient

# ✅ FIRST define app
app = Flask(__name__)

# ✅ THEN DB
client = MongoClient(os.environ.get("MONGO_URI"), serverSelectionTimeoutMS=5000)
db = client["tracker"]
collection = db["logs"]

# ✅ ROUTES AFTER app is defined

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

@app.route('/')
def home():
    return open("dashboard.html").read()

if __name__ == "__main__":
    app.run()
