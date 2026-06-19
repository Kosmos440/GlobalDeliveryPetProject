from unittest.mock import AsyncMock, patch

from tests.conftest import make_package


def test_post(client, override_session):
    json_data = {
        "package_id": "4a95e439-df10-4732-bf18-b117c0bf8fb1",
        "name": "Телефон Iphone 17 pro max",
        "weight": "0.3",
        "category_id": 2,
        "category_name": "Электроника",
        "value_usd": "1200",
        "delivery_cost_rub": "1219",
        "created_at": "2026-10-12T00:00:00",
    }
    package_data = {
        "name": "Телефон Iphone 17 pro max",
        "weight": 0.3,
        "category_id": 2,
        "value_usd": 1200.00,
    }
    mock_dal = AsyncMock()
    mock_dal.create_package.return_value = make_package()
    categories_mock_dal = AsyncMock()
    categories_mock_dal.get_id_in_categories.return_value = True
    with patch("app.services.package_service.PackageDAL") as mock_dal_cls, patch("app.services.package_service.PackageCategoryDAL") as categories_mock_cls:
        mock_dal_cls.return_value = mock_dal
        categories_mock_cls.return_value = categories_mock_dal
        response = client.post("/api/v1/package/", json=package_data)
    assert response.status_code == 200
    assert response.json() == json_data
    mock_dal.create_package.assert_awaited_once()


def test_post_create_error(client):
    package_data = {
        "weight": 0.3,
        "category_id": 2,
        "value_usd": 1200.00,
    }
    response = client.post("/api/v1/package/", json=package_data)
    assert response.status_code == 422

