"""Web app module for rock-paper-scissors game."""

import os
import random
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient("mongodb://mongodb:27017/")
db = client["rockPaperScissors"]


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
