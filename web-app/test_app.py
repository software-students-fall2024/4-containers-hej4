"""Tests for the Rock-Paper-Scissors web app."""
import sys
import os
from unittest.mock import patch, MagicMock
import pytest
from app import create_app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


@pytest.fixture
def client():
    """Create a test client"""
    test_config = {"TESTING": True, "MONGO_URI": "mongodb://localhost:27017/testdb"}
    app = create_app(test_config=test_config)
    with app.test_client() as client:
        yield client


def test_homepage(client):
    """Test homepage route status and content"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<h2>Player: 0</h2>" in response.data
    assert b"<h2>Computer: 0</h2>" in response.data


def test_play_game(client):
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
            "/store-result", json={"choice": "rock", "result": "win"}
        )
        assert response.status_code == 200
        mock_insert.assert_called_once_with({"choice": "rock", "result": "win"})


def test_play_route_invalid_method(client):
    """/play should only accept POST requests, not GET"""
    response = client.get("/play")
    assert response.status_code == 405
