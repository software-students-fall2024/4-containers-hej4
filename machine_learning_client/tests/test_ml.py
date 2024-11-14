import unittest
from unittest.mock import patch, MagicMock
from machine_learning_client.ml_app import fetch_image, get_player_rps

# Valid base64 encoded PNG image for testing
VALID_BASE64_IMAGE = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/"
    "w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
)


@patch("machine_learning_client.ml_app.db.images.find_one")
def test_fetch_image(mock_find_one):
    """Test fetch_image function with a mock database response."""
    mock_find_one.return_value = {
        "processed": False,
        "image": "test_image",
        "_id": "123",
    }
    image = fetch_image()
    assert image == {"processed": False, "image": "test_image", "_id": "123"}
    mock_find_one.assert_called_once_with({"processed": False}, sort=[("_id", -1)])


@patch(
    "machine_learning_client.ml_app.detector.findHands",
    return_value=(True, "modified_img"),
)
@patch("machine_learning_client.ml_app.detector.fingersUp")
def test_rps_rock(mock_fingers_up, mock_find_hands):
    """Test get_player_rps function when gesture represents 'rock'."""
    mock_fingers_up.return_value = [0, 0, 0, 0, 0]
    result = get_player_rps(VALID_BASE64_IMAGE)
    assert result == "rock"


@patch(
    "machine_learning_client.ml_app.detector.findHands",
    return_value=(True, "modified_img"),
)
@patch("machine_learning_client.ml_app.detector.fingersUp")
def test_rps_scissors(mock_fingers_up, mock_find_hands):
    """Test get_player_rps function when gesture represents 'scissors'."""
    mock_fingers_up.return_value = [0, 1, 1, 0, 0]
    result = get_player_rps(VALID_BASE64_IMAGE)
    assert result == "scissors"


@patch(
    "machine_learning_client.ml_app.detector.findHands",
    return_value=(True, "modified_img"),
)
@patch("machine_learning_client.ml_app.detector.fingersUp")
def test_rps_paper(mock_fingers_up, mock_find_hands):
    """Test get_player_rps function when gesture represents 'paper'."""
    mock_fingers_up.return_value = [1, 1, 1, 1, 1]
    result = get_player_rps(VALID_BASE64_IMAGE)
    assert result == "paper"


@patch("machine_learning_client.ml_app.detector.findHands", return_value=(None, None))
@patch("machine_learning_client.ml_app.detector.fingersUp")
def test_rps_no_hands(mock_fingers_up, mock_find_hands):
    """Test get_player_rps function when no hands are detected."""
    result = get_player_rps(VALID_BASE64_IMAGE)
    assert result == "no hands detected"


if __name__ == "__main__":
    unittest.main()
