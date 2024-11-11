"""Web app module for rock-paper-scissors game"""
from flask import Flask
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

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
