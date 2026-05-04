from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["tracker"]
collection = db["logs"]

@app.route('/log', methods=['POST'])
def log():
    data = request.json
    collection.insert_one(data)
    print("Saved:", data)
    return jsonify({"ok": True})

@app.route('/data', methods=['GET'])
def get_data():
    logs = list(collection.find({}, {"_id": 0}))
    return jsonify(logs)

# ✅ DASHBOARD ROUTE (must be OUTSIDE main block)
@app.route('/')
def home():
    return """
    <h2>Employee Activity Dashboard</h2>
    <div id="data"></div>

    <script>
    async function load() {
        let res = await fetch('/data');
        let data = await res.json();

        let html = "";
        data.forEach(item => {
            html += `<div style="border:1px solid #ccc; padding:10px; margin:5px;">
                <b>${item.user}</b><br>
                Site: ${item.domain}<br>
                Time: ${item.timestamp}
            </div>`;
        });

        document.getElementById("data").innerHTML = html;
    }

    setInterval(load, 3000);
    load();
    </script>
    """

# ✅ ONLY server run goes here
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)