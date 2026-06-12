import importlib
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    # Reload module to reset in-memory state between tests
    app_mod = importlib.import_module("src.app")
    importlib.reload(app_mod)
    return TestClient(app_mod.app)
