"""Web app module for rock-paper-scissors game."""

import os
import random
from flask import Flask, render_template, request, redirect, url_for, jsonify
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
        result = "win"
        return jsonify({"result": result})

    @app.route("/view_images")
    def view_images():
        """
        Route to view uploaded images
        Returns a list of all image data in JSON format
        """
        images = list(app.db.images.find({}, {"_id": 0, "image": 1}))
        return {"images": images}

    @app.route("/get_result", methods=["GET"])
    def get_result():
        image = app.db.images.find_one({"processed": True}, sort=[("processed_at", -1)])
        if image and "choice" in image:
            return jsonify({"choice": image["choice"]})
        return jsonify({"choice": "pending"})

    @app.route("/store-result", methods=["POST"])
    def store_result():
        data = request.json
        user_choice = data.get("user_choice")
        computer_choice = data.get("computer_choice")
        winner = data.get("winner")

        # Insert into MongoDB collection
        if all([user_choice, computer_choice, winner]):
            app.db.collection.insert_one(
                {
                    "user_choice": user_choice,
                    "computer_choice": computer_choice,
                    "winner": winner,
                }
            )
            return jsonify({"status": "success"}), 200
        return jsonify({"error": "Invalid data"}), 400

    @app.route("/display-rounds", methods=["GET"])
    def display_rounds():
        """
        Retrieve and display all historic rounds
        """
        rounds = list(app.db.collection.find({}, {"_id": 0}))
        for i, round_data in enumerate(rounds):
            round_data["round_number"] = i + 1

        if not rounds:
            return render_template(
                "result.html",
                rounds=[],
                stats={
                    "total_rounds": 0,
                    "user_wins": 0,
                    "computer_wins": 0,
                    "ties": 0,
                    "invalid": 0,
                    "user_win_percent": 0,
                    "computer_win_percent": 0,
                    "tie_percent": 0,
                    "invalid_percent": 0,
                },
                message="No rounds played yet",
            )

        # calculate stats
        num_rounds = len(rounds)
        user_wins = 0
        computer_wins = 0
        ties = 0
        invalid = 0
        for round_data in rounds:
            if round_data["winner"] == "player":
                user_wins += 1
            elif round_data["winner"] == "computer":
                computer_wins += 1
            elif round_data["winner"] == "tie":
                ties += 1
            if round_data["user_choice"] == "invalid choice":
                invalid += 1

        stats = {
            "total_rounds": num_rounds,
            "user_wins": user_wins,
            "computer_wins": computer_wins,
            "ties": ties,
            "invalid": invalid,
            "user_win_percent": (user_wins / num_rounds * 100) if num_rounds else 0,
            "computer_win_percent": (
                (computer_wins / num_rounds * 100) if num_rounds else 0
            ),
            "tie_percent": (ties / num_rounds * 100) if num_rounds else 0,
            "invalid_percent": (invalid / num_rounds * 100) if num_rounds else 0,
        }

        return render_template("result.html", rounds=rounds, stats=stats)

    return app


def random_rps():
    """returns random option: rocker, paper, or scissors"""
    options = ["rock", "paper", "scissors"]
    return random.choice(options)


def get_winner(player, comp):
    """returns game winner based on player and computer choices"""
    valid_choices = {"rock", "paper", "scissors"}
    if player not in valid_choices or comp not in valid_choices:
        return None
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
