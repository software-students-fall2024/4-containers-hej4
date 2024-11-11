"""Web app module for rock-paper-scissors game"""
from flask import Flask, request, jsonify
from pymongo import MongoClient

def create_app(test_config=None):
    """Create and configure app"""
    app = Flask(__name__)
    
    # database connection
    if test_config:
        # use different database/configuration for testing
        app.config.update(test_config)
        # local for testing
        client = MongoClient("mongodb://localhost:27017/")
    else:
        client = MongoClient("mongodb://mongodb:27017/")

    app.db = client["rockPaperScissors"]
    
    @app.route("/")
    def index():
        return "Welcome to Rock-Paper-Scissors"

    @app.route("/play", methods=["POST"])
    def play():
        user_choice = request.json.get("choice")
        result = "win"  # replace with actual logic, just using this for testing
        return jsonify({"result": result})

    @app.route("/store-result", methods=["POST"])
    def store_result():
        data = request.json
        choice = data.get("choice")
        result = data.get("result")

        # Insert into MongoDB collection
        if choice and result:
            app.db.collection.insert_one({"choice": choice, "result": result})
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"error": "Invalid data"}), 400


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
