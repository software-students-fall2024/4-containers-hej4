"""Web app module for rock-paper-scissors game."""

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017/")
db = client["rockPaperScissors"]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
