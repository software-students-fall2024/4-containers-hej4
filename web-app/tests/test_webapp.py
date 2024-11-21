"""Tests for the web app"""

# pylint: disable=redefined-outer-name
import sys
import os
from unittest.mock import patch, MagicMock
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from app import create_app, random_rps, get_winner


@pytest.fixture
def client():
    """Create a test client"""
    test_config = {"TESTING": True, "MONGO_URI": "mongodb://localhost:27017/testdb"}
    app = create_app(test_config=test_config)
    with app.test_client() as client:
        yield client


def test_homepage(client):  # pylint: disable=redefined-outer-name
    """Test homepage route status and content"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<h1>Let's Play Rock Paper Scissors!</h1>" in response.data
    assert b"<h2>Player</h2>" in response.data
    assert b"<h2>Computer</h2>" in response.data
    assert b'<button id="btn">GO!</button>' in response.data
    assert b'<video id="camera" autoplay playsinline></video>' in response.data


def test_play_game(client):  # pylint: disable=redefined-outer-name
    """Test play game route for expected outcomes with valid choice"""
    response = client.post("/play", json={"choice": "rock"})
    assert response.status_code == 200
    data = response.get_json()
    assert "result" in data
    assert data["result"] in ["win", "lose", "draw"]


def test_store_game_result(client):
    """Test storing game results in the database."""
    with patch.object(client.application, "db") as mock_db:
        mock_collection = mock_db.collection
        mock_insert = mock_collection.insert_one
        mock_insert.return_value = MagicMock(inserted_id="fake_id")

        response = client.post(
            "/store-result",
            json={
                "user_choice": "rock",
                "computer_choice": "scissors",
                "winner": "player",
            },
        )
        assert response.status_code == 200

        mock_insert.assert_called_once_with(
            {"user_choice": "rock", "computer_choice": "scissors", "winner": "player"}
        )


def test_play_route_invalid_method(client):
    """/play should only accept POST requests, not GET"""
    response = client.get("/play")
    assert response.status_code == 405


def test_store_result_invalid_data(client):
    """Test store result route with invalid data"""
    response = client.post("/store-result", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid data"


def test_upload_image(client):
    """Test image upload functionality"""
    with patch.object(client.application, "db") as mock_db:
        mock_images_collection = mock_db.images
        mock_insert = mock_images_collection.insert_one
        mock_insert.return_value = MagicMock(inserted_id="fake_id")

        response = client.post("/upload_image", json={"image": "mock_image_data"})
        assert response.status_code == 302
        mock_insert.assert_called_once_with(
            {"image": "mock_image_data", "processed": False}
        )


def test_random_rps():
    """Test random_rps helper function"""
    outcomes = {"rock", "paper", "scissors"}
    for _ in range(10):
        choice = random_rps()
        assert choice in outcomes


def test_get_winner():
    """Test get_winner function with all possible rps combinations"""
    assert get_winner("rock", "rock") == "tie"
    assert get_winner("rock", "scissors") == "player"
    assert get_winner("rock", "paper") == "comp"
    assert get_winner("paper", "rock") == "player"
    assert get_winner("paper", "scissors") == "comp"
    assert get_winner("scissors", "paper") == "player"
    assert get_winner("scissors", "rock") == "comp"
    assert get_winner("rock", "invalid") is None


def test_get_winner_invalid_input():
    """Test get_winner with invalid inputs"""
    assert get_winner("invalid", "rock") is None
    assert get_winner("invalid", "invalid") is None


def test_get_result(client):
    """Test get_result route"""
    with patch.object(client.application, "db") as mock_db:
        mock_images_collection = mock_db.images
        mock_images_collection.find_one.return_value = {
            "processed": True,
            "choice": "rock",
        }

        response = client.get("/get_result")
        assert response.status_code == 200
        data = response.get_json()
        assert data["choice"] == "rock"


def test_play_route_invalid_choice(client):
    """Test play route with invalid choice"""
    response = client.post("/play", json={"choice": "invalid_choice"})
    assert response.status_code == 200

    data = response.get_json()
    assert data["result"] in ["win", "lose", "draw"]


def test_display_rounds_empty(client):
    """Test display rounds when there are no rounds played yet"""
    with patch.object(client.application, "db") as mock_db:
        mock_collection = mock_db.collection
        mock_collection.find.return_value = []

        response = client.get("/display-rounds")
        assert response.status_code == 200
        assert b"No rounds played yet" in response.data


def test_get_result_no_image(client):
    """Test get_result route when there are no processed images"""
    with patch.object(client.application, "db") as mock_db:
        mock_images_collection = mock_db.images
        mock_images_collection.find_one.return_value = None

        response = client.get("/get_result")
        assert response.status_code == 200

        data = response.get_json()
        assert data["choice"] == "pending"


def test_view_images_empty(client):
    """Test viewing images when there are no images"""
    with patch.object(client.application, "db") as mock_db:
        mock_images_collection = mock_db.images
        mock_images_collection.find.return_value = []

        response = client.get("/view_images")
        assert response.status_code == 200

        data = response.get_json()
        assert "images" in data
        assert data["images"] == []


def test_display_rounds_mixed_data(client):
    """Test display rounds when there is a mix of valid and invalid rounds"""
    with patch.object(client.application, "db") as mock_db:
        mock_collection = mock_db.collection
        mock_collection.find.return_value = [
            {"user_choice": "rock", "computer_choice": "scissors", "winner": "player"},
            {
                "user_choice": "invalid choice",
                "computer_choice": "rock",
                "winner": "tie",
            },
        ]
        response = client.get("/display-rounds")
        assert response.status_code == 200
        assert b"rock" in response.data
        assert b"scissors" in response.data
        assert b"tie" in response.data
