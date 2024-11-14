"""Test Cases for the Rock-Paper-Scissors web app."""

import sys
import os
from unittest.mock import patch, MagicMock
import pytest
from web_app import create_app, random_rps, get_winner

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


@pytest.fixture
def test_client():
    """Create a test client"""
    test_config = {"TESTING": True, "MONGO_URI": "mongodb://localhost:27017/testdb"}
    app = create_app(test_config=test_config)
    with app.test_client() as client:
        yield client


def test_homepage(test_client):
    """Test homepage route status and content"""
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"<h2>Player: 0</h2>" in response.data
    assert b"<h2>Computer: 0</h2>" in response.data


def test_play_game(test_client):
    """Test play game route for expected outcomes with valid choice"""
    response = test_client.post("/play", json={"choice": "rock"})
    assert response.status_code == 200
    data = response.get_json()
    assert "result" in data
    assert data["result"] in ["win", "lose", "draw"]


def test_store_game_result(test_client):
    """Test storing game results in the database."""
    with patch.object(test_client.application, "db") as mock_db:
        mock_collection = mock_db.collection
        mock_insert = mock_collection.insert_one
        mock_insert.return_value = MagicMock(inserted_id="fake_id")

        response = test_client.post(
            "/store-result", json={"choice": "rock", "result": "win"}
        )
        assert response.status_code == 200
        mock_insert.assert_called_once_with({"choice": "rock", "result": "win"})


def test_play_route_invalid_method(test_client):
    """/play should only accept POST requests, not GET"""
    response = test_client.get("/play")
    assert response.status_code == 405


def test_store_result_invalid_data(test_client):
    """Test store result route with invalid data"""
    response = test_client.post("/store-result", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid data"


def test_upload_image(test_client):
    """Test image upload functionality"""
    with patch.object(test_client.application, "db") as mock_db:
        mock_images_collection = mock_db.images
        mock_insert = mock_images_collection.insert_one
        mock_insert.return_value = MagicMock(inserted_id="fake_id")

        response = test_client.post("/upload_image", json={"image": "mock_image_data"})
        assert response.status_code == 302  # Redirect to home
        mock_insert.assert_called_once_with({"image": "mock_image_data"})


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
