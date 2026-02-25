import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities as _activities


@pytest.fixture
def original_activities():
    return copy.deepcopy(_activities)


@pytest.fixture(autouse=True)
def reset_activities(original_activities):
    # Replace in-memory activities with a fresh copy before each test
    _activities.clear()
    _activities.update(copy.deepcopy(original_activities))
    yield


@pytest.fixture
def client():
    return TestClient(app)
