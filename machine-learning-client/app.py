"""Machine learnin app module for rock-paper-scissors game."""

from pymongo import MongoClient

client = MongoClient("mongodb://mongodb:27017/")
db = client["rockPaperScissors"]
