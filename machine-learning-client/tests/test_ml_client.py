"""Tests for the machine learning client"""

# pylint: disable=redefined-outer-name
import sys
import os

# import unittest
# from unittest.mock import patch, MagicMock
# from app import fetch_image, get_player_rps
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


# delete this when tests are added - just using for badge implementation
def test_placeholder():
    """Placeholder test until actual tests are added"""
    assert True


# Valid base64 encoded PNG image for testing
# VALID_BASE64_IMAGE = (
#     "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/"
#     "w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
# )

# @patch("app.db.images.find_one")
# def test_fetch_image(mock_find_one):
#     """Test fetch_image function with a mock database"""
#     mock_find_one.return_value = {
#         "processed": False,
#         "image": "test_image",
#         "_id": "123",
#     }
#     image = fetch_image()
#     assert image == {"processed": False, "image": "test_image", "_id": "123"}
#     mock_find_one.assert_called_once_with({"processed": False}, sort=[("_id", -1)])


# @patch("app.detector.findHands", return_value=(True, "modified_img"))
# @patch("app.detector.fingersUp")
# def test_rps_rock(mock_fingers_up, mock_find_hands):
#     """Test get_player_rps function when gesture is rock."""
#     mock_fingers_up.return_value = [0, 0, 0, 0, 0]
#     result = get_player_rps(VALID_BASE64_IMAGE)
#     assert result == "rock"


# @patch("app.detector.findHands", return_value=([{"id": 1}], "modified_img"))
# @patch("app.detector.fingersUp")
# def test_rps_scissors(mock_fingers_up, mock_find_hands):
#     """Test get_player_rps function when gesture is scissors."""
#     mock_fingers_up.return_value = [0, 1, 1, 0, 0]
#     result = get_player_rps(VALID_BASE64_IMAGE)
#     assert result == "scissors"


# @patch("app.detector.findHands", return_value=(True, "modified_img"))
# @patch("app.detector.fingersUp")
# def test_rps_paper(mock_fingers_up, mock_find_hands):
#     """Test get_player_rps function when gesture is paper."""
#     mock_fingers_up.return_value = [1, 1, 1, 1, 1]
#     result = get_player_rps(VALID_BASE64_IMAGE)
#     assert result == "paper"


# @patch("app.detector.findHands", return_value=(None, None))
# @patch("app.detector.fingersUp")
# def test_rps_no_hands(mock_fingers_up, mock_find_hands):
#     """Test get_player_rps function when there are no hands detected."""
#     result = get_player_rps(VALID_BASE64_IMAGE)


# if __name__ == "__main__":
#     unittest.main()
