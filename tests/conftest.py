import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module

# Preserve a deep copy of the original activities so tests can reset state
_ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory `activities` dict before each test."""
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))


@pytest.fixture
def client():
    """Provide a TestClient instance for the FastAPI app."""
    with TestClient(app_module.app) as c:
        yield c
