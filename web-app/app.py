"""Web app module for rock-paper-scissors game."""

import os
import random
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient("mongodb://mongodb:27017/")
db = client["rockPaperScissors"]

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


def random_rps():
    """returns random option: rocker, paper, or scissors"""
    options = ["rock", "paper", "scissors"]
    return random.choice(options)


def get_winner(player, comp):
    """returns game winner based on player and computer choices"""
    outcomes = {
        "rock": {"scissors": "player", "paper": "comp"},
        "paper": {"rock": "player", "scissors": "comp"},
        "scissors": {"paper": "player", "rock": "comp"},
    }
    return "tie" if player == comp else outcomes.get(player, {}).get(comp, None)


def create_app():
    """creates and sets up flask app and routes"""
    app = Flask(__name__)

    @app.route("/")
    def home():
        """
        Route for game
        Returns rendered html template
        """
        return render_template("index.html")

    @app.route("/upload_image", methods=["POST"])
    def upload_image():
        """
        Route for game
        Uploads image to mongodb
        """
        data = request.get_json()
        image_data = data["image"]
        db.images.insert_one({"image": image_data})
        print("inserted image: ", image_data)

        return redirect(url_for("home"))

    return app


if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    flask_app = create_app()
    flask_app.run(port=FLASK_PORT)
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
