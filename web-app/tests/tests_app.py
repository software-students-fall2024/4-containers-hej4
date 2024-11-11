"""Tests for the web app."""
from unittest.mock import patch, MagicMock
import pytest
from app import create_app

# configure test client to simulate requests to flask app
@pytest.fixture
def client():
    app = create_app(test_config=True)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

# test home page route
def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Rock-Paper-Scissors" in response.data

# test that play game page shows valid game outcome
def test_play_game(client):
    response = client.post("/play", json={"choice": "rock"})
    assert response.status_code == 200

    data = response.get_json()
    # where result = game outcome
    assert "result" in data
    assert data["result"] in ["win", "lose", "draw"]

# test database interactions (specifically with insert_one)
def test_store_game_result(client):
    with patch("app.db.collection.insert_one") as mock_insert:
        mock_insert.return_value = MagicMock(inserted_id="fake_id")

        response = client.post("/store-result", json={"choice": "rock", "result": "win"})
        assert response.status_code == 200

        # check that insert_one was called with expected data
        mock_insert.assert_called_once_with({"choice": "rock", "result": "win"})