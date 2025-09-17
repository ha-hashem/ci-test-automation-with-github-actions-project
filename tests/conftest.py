import sys
import os
import pytest

from starlette.testclient import TestClient
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client
