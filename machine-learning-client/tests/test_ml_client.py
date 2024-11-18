"""Tests for the machine learning client"""

# pylint: disable=redefined-outer-name
import sys
import os
import unittest
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from app import fetch_image, get_player_rps

# Valid base64 encoded PNG image for testing
VALID_BASE64_IMAGE = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/"
    "w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
)

@patch("app.detector.findHands", return_value=([{"id": 1}], "modified_img"))
@patch("app.detector.fingersUp", return_value=[0, 0, 0, 0, 0])
def test_rps_rock(mock_fingers_up, mock_find_hands):
    """Test get_player_rps function when gesture is rock."""
    result, hands, fingers = get_player_rps(VALID_BASE64_IMAGE)
    assert result == "rock"
    assert fingers == [0, 0, 0, 0, 0]

@patch("app.detector.findHands", return_value=([{"id": 1}], "modified_img"))
@patch("app.detector.fingersUp", return_value=[0, 1, 1, 0, 0])
def test_rps_scissors(mock_fingers_up, mock_find_hands):
    """Test get_player_rps function when gesture is scissors."""
    result, hands, fingers = get_player_rps(VALID_BASE64_IMAGE)
    assert result == "scissors"
    assert fingers == [0, 1, 1, 0, 0]

@patch("app.detector.findHands", return_value=([{"id": 1}], "modified_img"))
@patch("app.detector.fingersUp", return_value=[1, 1, 1, 1, 1])
def test_rps_paper(mock_fingers_up, mock_find_hands):
    """Test get_player_rps function when gesture is paper."""
    result, hands, fingers = get_player_rps(VALID_BASE64_IMAGE)
    assert result == "paper"
    assert fingers == [1, 1, 1, 1, 1]

@patch("app.detector.findHands", return_value=(None, None))
@patch("app.detector.fingersUp")
def test_rps_no_hands(mock_fingers_up, mock_find_hands):
    """Test get_player_rps function when there are no hands detected."""
    result = get_player_rps(VALID_BASE64_IMAGE)
    assert result[0] == "no hands detected"  # Updated assertion
    mock_fingers_up.assert_not_called()  # fingersUp shouldn't be called if no hands detected

if __name__ == "__main__":
    unittest.main()
