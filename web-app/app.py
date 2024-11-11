"""Web app module for rock-paper-scissors game."""

import os
from flask import Flask, render_template
from pymongo import MongoClient
import random

client = MongoClient("mongodb://mongodb:27017/")
db = client["rockPaperScissors"]

# todo: write tests for these
def random_rps():
    options = ["rock", "paper", "scissors"]
    return random.choice(options)

def get_winner(player, comp):
    if player == comp:
        return "tie"
    elif player == "rock":
        if comp == "scissors":
            return "player"
        elif comp == "paper":
            return "comp"
    elif player == "paper":
        if comp == "rock":
            return "player"
        elif comp == "scissors":
            return "comp"
    elif player == "scissors":
        if comp == "paper":
            return "player"
        elif comp == "rock":
            return "comp"

def create_app():
    app = Flask(__name__)
    
    @app.route("/")
    def home():
        """
        Route for home page
        Returns:
            rendered html template
        """
        return render_template("index.html")
    
    return app

if __name__ == '__main__':
    FLASK_PORT = os.getenv("FLASK_PORT", "5000")
    app = create_app()
    app.run(port=FLASK_PORT)