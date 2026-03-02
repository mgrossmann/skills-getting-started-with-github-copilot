import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Ensure each test sees the original activity data."""
    snapshot = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(snapshot))


@pytest.fixture()
def client():
    """FastAPI test client bound to the app under test."""
    return TestClient(app)
