from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import unquote
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

try:
    # new client and connect to server
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["ai-gateway-backend"]
    tools_collection = db["tools"]
    print("Connected successfully!")
    print("Databases:", client.list_database_names())
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

# get all ai tools
@app.route("/tools", methods=["GET"])
def get_tools():
    tools = list(tools_collection.find({}, {"_id": 0}))
    return jsonify(tools)

# get ai tools by category
@app.route("/tools/category/<category>", methods=["GET"])
def get_tools_by_category(category):
    category = unquote(category)
    if not category:
        return jsonify({"error": "Valid category is required"}), 400

    tools = list(tools_collection.find({"category" : category}, {"_id" : 0}))
    return jsonify(tools)

# Route to serve static icons
@app.route('/static/icons/<filename>')
def serve_icon(filename):
    return send_from_directory('data/static/icons', filename)

if __name__ == "__main__":
    app.run(debug=True)
