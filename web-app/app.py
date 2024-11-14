"""Web app module for rock-paper-scissors game."""

import os
import random
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

# todo: write tests for these


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

    # CORS(app, support_credentials=True)
    # CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

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
        app.db.images.insert_one({"image": image_data, "processed": False})

        return redirect(url_for("home"))

    @app.route("/play", methods=["POST"])
    def play():
        user_choice = request.json.get("choice")
        print(user_choice)
        result = "win"  # replace with actual logic, just using this for testing
        return jsonify({"result": result})

    @app.route("/view_images")
    def view_images():
        """
        Route to view uploaded images
        Returns a list of all image data in JSON format
        """
        images = list(
            app.db.images.find({}, {"_id": 0, "image": 1})
        )  # Exclude _id for simplicity
        return {"images": images}

    # for debugging
    @app.route("/get_result", methods=["GET"])
    def get_result():
        image = app.db.images.find_one({"processed": True}, sort=[("processed_at", -1)])
        if image and "choice" in image:
            return jsonify({"choice": image["choice"]})
        return jsonify({"choice": "pending"})

    @app.route("/store-result", methods=["POST"])
    def store_result():
        data = request.json
        choice = data.get("choice")
        result = data.get("result")

        # Insert into MongoDB collection
        if choice and result:
            app.db.collection.insert_one({"choice": choice, "result": result})
            return jsonify({"status": "success"}), 200
        return jsonify({"error": "Invalid data"}), 400

    return app


def random_rps():
    """returns random option: rocker, paper, or scissors"""
    options = ["rock", "paper", "scissors"]
    return random.choice(options)


def get_winner(player, comp):
    """returns game winner based on player and computer choices"""
    valid_choices = {"rock", "paper", "scissors"}
    if player not in valid_choices or comp not in valid_choices:
        return None  # Handle invalid input
    outcomes = {
        "rock": {"scissors": "player", "paper": "comp"},
        "paper": {"rock": "player", "scissors": "comp"},
        "scissors": {"paper": "player", "rock": "comp"},
    }
    return "tie" if player == comp else outcomes.get(player, {}).get(comp, None)


if __name__ == "__main__":
    FLASK_PORT = os.getenv("FLASK_PORT", "5001")
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5001, debug=True)
    # added host
    # app.run(host="0.0.0.0", port=FLASK_PORT)
