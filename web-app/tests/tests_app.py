"""Tests for the web app"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from unittest.mock import patch, MagicMock
import pytest
from app import create_app


@pytest.fixture
def client():
    """Create a test client"""
    test_config = {"TESTING": True, "MONGO_URI": "mongodb://localhost:27017/testdb"}
    app = create_app(test_config=test_config)
    with app.test_client() as client:
        yield client


def test_homepage(client):  # pylint: disable=redefined-outer-name
    """Test  homepage route status and content"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Rock-Paper-Scissors" in response.data


def test_play_game(client):  # pylint: disable=redefined-outer-name
    """Test play game route for expected outcomes with valid choice"""
    response = client.post("/play", json={"choice": "rock"})
    assert response.status_code == 200
    data = response.get_json()
    assert "result" in data
    assert data["result"] in ["win", "lose", "draw"]


def test_store_game_result(client):
    """Test storing game results in the database."""
    with patch.object(client.application, 'db') as mock_db:
        mock_collection = mock_db.collection
        mock_insert = mock_collection.insert_one
        mock_insert.return_value = MagicMock(inserted_id="fake_id")
        
        response = client.post("/store-result", json={"choice": "rock", "result": "win"})
        assert response.status_code == 200
        mock_insert.assert_called_once_with({"choice": "rock", "result": "win"})
        