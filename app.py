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

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Employee Tracker</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f5f7fa;
                margin: 0;
                padding: 0;
            }

            .header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: #1e293b;
                color: white;
                padding: 15px 30px;
            }

            .header h1 {
                margin: 0;
                font-size: 20px;
            }

            .logo {
                height: 40px;
            }

            .container {
                padding: 20px;
                max-width: 900px;
                margin: auto;
            }

            .card {
                background: white;
                border-radius: 10px;
                padding: 15px 20px;
                margin-bottom: 15px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                transition: 0.2s;
            }

            .card:hover {
                transform: scale(1.01);
            }

            .user {
                font-weight: bold;
                font-size: 16px;
                color: #1e293b;
            }

            .domain {
                color: #2563eb;
                margin-top: 5px;
            }

            .time {
                color: gray;
                font-size: 12px;
                margin-top: 5px;
            }
        </style>
    </head>

    <body>

        <div class="header">
            <h1>Employee Activity Dashboard</h1>

            <!-- 🔥 ADD YOUR LOGO HERE -->
            <img src="https://media.licdn.com/dms/image/v2/D4D0BAQF5ABpfcNZB4w/company-logo_200_200/company-logo_200_200/0/1692003695229/infividhya_logo?e=2147483647&v=beta&t=Y5zboVYxQyIRa9y4DrAiYXpjva6-vCvRlxQw5rjvxFk" class="logo">
        </div>

        <div class="container">
            <div id="data"></div>
        </div>

        <script>
        async function load() {
            let res = await fetch('/data?nocache=' + new Date().getTime());
            let data = await res.json();

            let html = "";

            data.forEach(item => {
                let localTime = new Date(item.timestamp).toLocaleString();

                html += `
                    <div class="card">
                        <div class="user">${item.name} (${item.user})</div>
                        <div class="domain">🌐 ${item.domain}</div>
                        <div class="time">🕒 ${localTime}</div>
                    </div>
                `;
            });

            document.getElementById("data").innerHTML = html;
        }

        setInterval(load, 3000);
        load();
        </script>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run()
