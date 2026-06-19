import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, patch

from tests.conftest import make_package


def test_get_by_id(client, override_session):
    mock_dal = AsyncMock()
    mock_dal.get_package_by_id.return_value = make_package(
        name="Ноутбук Acer",
        weight=Decimal("4"),
        value_usd=Decimal("1500"),
    )

    with patch("app.services.package_service.PackageDAL") as mock_dal_cls:
        mock_dal_cls.return_value = mock_dal
        response = client.get("/api/v1/package/4a95e439-df10-4732-bf18-b117c0bf8fb1")

    assert response.status_code == 200
    assert response.json() == {
        "package_id": "4a95e439-df10-4732-bf18-b117c0bf8fb1",
        "name": "Ноутбук Acer",
        "weight": "4",
        "category_id": 2,
        "category_name": "Электроника",
        "value_usd": "1500",
        "delivery_cost_rub": "1219",
        "created_at": "2026-10-12T00:00:00",
    }


def test_get_by_session(client, override_session):
    session_id = uuid.UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
    packages = [
        make_package(name="Ноутбук Acer"),
        make_package(
            package_id=uuid.UUID("1cf8b169-1c42-4e55-9e10-7597b0d9afdc"),
            name="Ноутбук HP",
            delivery_cost_rub=789,
        ),
        make_package(
            package_id=uuid.UUID("3b073586-61a0-4fed-8c10-fff79bfb8df0"),
            name="Телефон Iphone 17 pro max",
            delivery_cost_rub=861,
        ),
    ]

    mock_dal = AsyncMock()
    mock_dal.get_filtered_packages_by_session.return_value = packages

    client.cookies.set("session_id", str(session_id))

    with patch("app.services.package_service.PackageDAL") as mock_dal_cls:
        mock_dal_cls.return_value = mock_dal
        response = client.get("/api/v1/package/")

    assert response.status_code == 200
    assert response.json() == {
        'packages': [
            {
                'package_id': '4a95e439-df10-4732-bf18-b117c0bf8fb1',
                'name': 'Ноутбук Acer',
                'weight': '0.3',
                'category_name': 'Электроника',
                'value_usd': '1200',
                'delivery_cost_rub': '1219',
                'created_at': '2026-10-12T00:00:00'},
            {
                'package_id': '1cf8b169-1c42-4e55-9e10-7597b0d9afdc',
                'name': 'Ноутбук HP',
                'weight': '0.3',
                'category_name': 'Электроника',
                'value_usd': '1200',
                'delivery_cost_rub': '789',
                'created_at': '2026-10-12T00:00:00'},
            {
                'package_id': '3b073586-61a0-4fed-8c10-fff79bfb8df0',
                'name': 'Телефон Iphone 17 pro max',
                'weight': '0.3',
                'category_name': 'Электроника',
                'value_usd': '1200',
                'delivery_cost_rub': '861',
                'created_at': '2026-10-12T00:00:00'}
        ],
        'current_page': 1,
        'total_pages': 1,
        'page_size': 5,
     }

    mock_dal.get_filtered_packages_by_session.assert_awaited_once_with(
        session_id=session_id,
        page=1,
        size=5,
        column=None,
        change_direction=False,
        search=None,
        category_id=None,
        min_weight=None,
        max_weight=None,
        min_value=None,
        max_value=None
    )
