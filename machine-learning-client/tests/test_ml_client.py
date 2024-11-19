"""Tests for the machine learning client"""

# pylint: disable=redefined-outer-name
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from app import get_player_rps, fetch_image

# valid base64 image string
VALID_BASE64_IMAGE = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/"
    "w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
)


@patch("app.detector.findHands", return_value=([{"id": 1}], "modified_img"))
@patch("app.detector.fingersUp", return_value=[0, 0, 0, 0, 0])
def test_rps_rock(_mock_fingers_up, _mock_find_hands):
    """Test get_player_rps function when gesture is rock."""
    result, _, fingers = get_player_rps(VALID_BASE64_IMAGE)
    assert result == "rock"
    assert fingers == [0, 0, 0, 0, 0]


@patch("app.detector.findHands", return_value=([{"id": 1}], "modified_img"))
@patch("app.detector.fingersUp", return_value=[0, 1, 1, 0, 0])
def test_rps_scissors(_mock_fingers_up, _mock_find_hands):
    """Test get_player_rps function when gesture is scissors."""
    result, _, fingers = get_player_rps(VALID_BASE64_IMAGE)
    assert result == "scissors"
    assert fingers == [0, 1, 1, 0, 0]


@patch("app.detector.findHands", return_value=([{"id": 1}], "modified_img"))
@patch("app.detector.fingersUp", return_value=[1, 1, 1, 1, 1])
def test_rps_paper(_mock_fingers_up, _mock_find_hands):
    """Test get_player_rps function when gesture is paper."""
    result, _, fingers = get_player_rps(VALID_BASE64_IMAGE)
    assert result == "paper"
    assert fingers == [1, 1, 1, 1, 1]


@patch("app.detector.findHands", return_value=(None, None))
@patch("app.detector.fingersUp")
def test_rps_no_hands(mock_fingers_up, _mock_find_hands):
    """Test get_player_rps function when there are no hands detected."""
    result = get_player_rps(VALID_BASE64_IMAGE)
    assert result[0] == "no hands detected"
    mock_fingers_up.assert_not_called()


@patch("app.detector.findHands", return_value=([{"id": 1}], "modified_img"))
@patch("app.detector.fingersUp", return_value=[1, 0, 1, 0, 1])
def test_invalid_gesture(_mock_fingers_up, _mock_find_hands):
    """Test get_player_rps function when gesture is invalid."""
    result, _, fingers = get_player_rps(VALID_BASE64_IMAGE)
    assert result == "invalid choice"
    assert fingers == [1, 0, 1, 0, 1]


@patch("app.db")
def test_fetch_image(mock_db):
    """Test fetch_image function when there are unprocessed and no unprocessed images."""
    mock_collection = MagicMock()
    mock_db.images = mock_collection

    mock_collection.find_one.return_value = {
        "_id": "123",
        "image": "sample_base64_image",
        "processed": False,
    }
    result = fetch_image()
    assert result == {"_id": "123", "image": "sample_base64_image", "processed": False}
    mock_collection.find_one.assert_called_with(
        {"processed": False}, sort=[("_id", -1)]
    )

    mock_collection.find_one.return_value = None
    result = fetch_image()
    assert result is None
    mock_collection.find_one.assert_called_with(
        {"processed": False}, sort=[("_id", -1)]
    )


def test_corrupted_image_data():
    """Test get_player_rps function with corrupted base64 image data."""
    corrupted_image = "data:image/png;base64,INVALID_BASE64_DATA"
    result, hands, fingers = get_player_rps(corrupted_image)
    assert result == "invalid choice"
    assert hands is None
    assert fingers is None


@patch("app.detector.findHands", return_value=(None, None))
def test_empty_image_data(_mock_find_hands):
    """Test get_player_rps function with an empty base64 image string."""
    result, hands, fingers = get_player_rps("")
    assert result == "invalid choice"
    assert hands is None
    assert fingers is None


@patch("app.detector.findHands", side_effect=RuntimeError("Detector error"))
@patch("app.detector.fingersUp")
def test_hand_detection_exception(mock_fingers_up, _mock_find_hands):
    """Test get_player_rps function when findHands raises an exception."""
    try:
        result, hands, fingers = get_player_rps(VALID_BASE64_IMAGE)
    except RuntimeError:
        result = "invalid choice"
        hands = None
        fingers = None

    assert result == "invalid choice"
    assert hands is None
    assert fingers is None
    mock_fingers_up.assert_not_called()


@patch("app.detector.findHands", return_value=([{"id": 1}], "modified_img"))
@patch("app.detector.fingersUp", return_value=[0, 1, 0, 1, 0])
def test_ambiguous_hand_gesture(_mock_fingers_up, _mock_find_hands):
    """Test get_player_rps function with a hard to hand gesture."""
    result, _, fingers = get_player_rps(VALID_BASE64_IMAGE)
    assert result == "invalid choice"
    assert fingers == [0, 1, 0, 1, 0]


@patch("app.db")
def test_no_unprocessed_images(mock_db):
    """Test fetch_image function when no unprocessed images is present."""
    mock_db.images.find_one.return_value = None
    result = fetch_image()
    assert result is None
    mock_db.images.find_one.assert_called_once_with(
        {"processed": False}, sort=[("_id", -1)]
    )


@patch("app.db")
def test_unexpected_image_format(mock_db):
    """Test fetch_image function with invalid image format."""
    mock_db.images.find_one.return_value = {
        "_id": "123",
        "image": None,
        "processed": False,
    }
    result = fetch_image()
    assert result == {"_id": "123", "image": None, "processed": False}
    mock_db.images.find_one.assert_called_once_with(
        {"processed": False}, sort=[("_id", -1)]
    )


@patch("app.detector.findHands", return_value=([{"id": 1}], "modified_img"))
@patch("app.detector.fingersUp", return_value=[1, 0, 1, 0, 1])
def test_multiple_invalid_gestures(_mock_fingers_up, _mock_find_hands):
    """Test get_player_rps function multiple times with invalid gestures."""
    for _ in range(3):  # multiple invalid inputs
        result, _, fingers = get_player_rps(VALID_BASE64_IMAGE)
        assert result == "invalid choice"
        assert fingers == [1, 0, 1, 0, 1]


@patch("app.detector.findHands", return_value=(None, None))
def test_no_hands_and_corrupted_data(_mock_find_hands):
    """Test get_player_rps function when no hands are detected and the image data is corrupted."""
    corrupted_image = "data:image/png;base64,INVALID_DATA"
    result, hands, fingers = get_player_rps(corrupted_image)
    assert result == "invalid choice"
    assert hands is None
    assert fingers is None


if __name__ == "__main__":
    unittest.main()
