# """Tests for the machine learning client"""

# # pylint: disable=redefined-outer-name
# import sys
# import os
# import unittest
# from unittest.mock import patch
# from app import get_player_rps  

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# # Valid base64 encoded PNG image for testing
# VALID_BASE64_IMAGE = (
#     "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/"
#     "w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
# )


# @patch("app.detector.fingersUp", return_value=[0, 0, 0, 0, 0])
# def test_rps_rock(mock_fingers_up):
#     """Test get_player_rps function when gesture is rock."""
#     result = get_player_rps(VALID_BASE64_IMAGE)
#     assert result == "rock"  


# @patch("app.detector.fingersUp", return_value=[0, 1, 1, 0, 0])
# def test_rps_scissors(mock_fingers_up):
#     """Test get_player_rps function when gesture is scissors."""
#     result = get_player_rps(VALID_BASE64_IMAGE)
#     assert result == "scissors"  


# @patch("app.detector.fingersUp", return_value=[1, 1, 1, 1, 1])
# def test_rps_paper(mock_fingers_up):
#     """Test get_player_rps function when gesture is paper."""
#     result = get_player_rps(VALID_BASE64_IMAGE)
#     assert result == "paper" 


# @patch("app.detector.findHands", return_value=(None, None))
# def test_rps_no_hands(mock_find_hands):  # noqa: W0613
#     """Test get_player_rps function when there are no hands detected."""
#     result = get_player_rps(VALID_BASE64_IMAGE)
#     assert result == "no hands detected"  


# if __name__ == "__main__":
#     unittest.main()
