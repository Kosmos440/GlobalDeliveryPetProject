import uuid
from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.db.session import get_session
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def override_session():
    mock_session = AsyncMock()

    async def _override():
        yield mock_session

    app.dependency_overrides[get_session] = _override
    yield mock_session
    app.dependency_overrides.pop(get_session, None)


def make_package(**kwargs):
    defaults = {
        "package_id": uuid.UUID("4a95e439-df10-4732-bf18-b117c0bf8fb1"),
        "name": "Телефон Iphone 17 pro max",
        "weight": Decimal("0.3"),
        "category_id": 2,
        "category_name": "Электроника",
        "value_usd": Decimal("1200"),
        "delivery_cost_rub": Decimal("1219"),
        "created_at": datetime(year=2026, month=10, day=12),
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)
