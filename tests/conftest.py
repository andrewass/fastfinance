import pytest
from fastapi.testclient import TestClient

from app.cache.cachedecorator import clear_cache
from app.main import app
from app.settings.settings import settings


@pytest.fixture(autouse=True)
def disable_cache(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(settings, "cache_enabled", False)
    clear_cache()
    yield
    clear_cache()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
