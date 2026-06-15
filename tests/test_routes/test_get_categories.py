from types import SimpleNamespace
from unittest.mock import AsyncMock, patch


def test_get_categories(client, override_session):
    categories = [
        SimpleNamespace(id=1, category_name="Одежда"),
        SimpleNamespace(id=2, category_name="Электроника"),
        SimpleNamespace(id=3, category_name="Другое"),
    ]
    mock_dal = AsyncMock()
    mock_dal.get_all_categories.return_value = categories

    with patch("app.api.v1.routers.package_categories.PackageCategoryDAL") as mock_dal_cls:
        mock_dal_cls.return_value = mock_dal
        response = client.get("/api/v1/categories/")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "category_name": "Одежда"},
        {"id": 2, "category_name": "Электроника"},
        {"id": 3, "category_name": "Другое"},
    ]
