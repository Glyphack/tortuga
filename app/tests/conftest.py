import pytest
from starlette.testclient import TestClient

from app.api.services.game_services.service import create_new_game
from app.helpers.jwt_helper import create_access_token
from main import app


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def auth_header_generator():
    def _auth_header_generator(name):
        token = create_access_token({"username": name}).decode("utf-8")
        header = {"Authorization": f"bearer {token}",
                  "Content-Type": "application/json"}
        return header

    return _auth_header_generator


@pytest.fixture
def game():
    return create_new_game("1", ["p1", "p2", "p3", "p4"], "p2")
