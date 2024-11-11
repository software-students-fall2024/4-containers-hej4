"""Tests for the web app"""

import sys
from unittest.mock import patch, MagicMock
import pytest
sys.path.append('../web-app')
from app import create_app

@pytest.fixture
def client():
    """Create a test client"""
    app = create_app(test_config=True)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test  homepage route status and content"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Rock-Paper-Scissors" in response.data

def test_play_game(client):
    """Test play game route for expected outcomes with valid choice"""
    response = client.post("/play", json={"choice": "rock"})
    assert response.status_code == 200
    data = response.get_json()
    assert "result" in data
    assert data["result"] in ["win", "lose", "draw"]

def test_store_game_result(client):
    """Test storing results in database"""
    with patch("app.db.collection.insert_one") as mock_insert:
        mock_insert.return_value = MagicMock(inserted_id="fake_id")
        response = client.post("/store-result", json={"choice": "rock", "result": "win"})
        assert response.status_code == 200
        mock_insert.assert_called_once_with({"choice": "rock", "result": "win"})
