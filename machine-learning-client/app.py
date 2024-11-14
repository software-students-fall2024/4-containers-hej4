"""
Machine learning app module for rock-paper-scissors game
Inspired by: https://github.com/Assem-ElQersh/Rock-Paper-Scissors-Game
"""

from pymongo import MongoClient
import time
import cv2
from cvzone.HandTrackingModule import HandDetector
from datetime import datetime
import base64
import numpy as np

client = MongoClient("mongodb://mongodb:27017/")
db = client["rockPaperScissors"]

detector = HandDetector(maxHands=1)


def fetch_image():
    """
    Try to fetch unprocessed image from MongoDB
    """
    image = db.images.find_one({"processed": False}, sort=[("_id", -1)])
    return image


def get_player_rps(image_data):
    """
    Analyze image, return player choice
    """
    image_data = base64.b64decode(image_data.split(",")[1])
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    hands, img = detector.findHands(img)
    if not hands:
        return "no hands detected"

    fingers = detector.fingersUp(hands[0])
    if fingers == [0, 0, 0, 0, 0]:
        return "rock"
    elif fingers == [1, 1, 1, 1, 1]:
        return "paper"
    elif fingers == [0, 1, 1, 0, 0]:
        return "scissors"

    return "invalid choice"


def main():
    """
    Poll for unprocessed image
    If unprocessed image is found,
    process it and update the image document with results
    """
    while True:
        image_doc = fetch_image()
        if image_doc:
            player_choice = get_player_rps(image_doc["image"])
            if player_choice:
                db.images.update_one(
                    {"_id": image_doc["_id"]},
                    {
                        "$set": {
                            "processed": True,
                            "choice": player_choice,
                            "processed_at": datetime.utcnow(),  # Add timestamp
                        }
                    },
                )

        # fetch image every second
        time.sleep(1)


if __name__ == "__main__":
    main()
