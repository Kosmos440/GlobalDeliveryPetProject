import uuid

from starlette.requests import Request
from starlette.responses import Response

from app.core.session_manager import get_session_id


def _make_request(cookies: dict[str, str] | None = None) -> Request:
    headers = []
    if cookies:
        cookie_header = "; ".join(f"{key}={value}" for key, value in cookies.items())
        headers.append((b"cookie", cookie_header.encode()))

    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "path": "/",
        "headers": headers,
        "query_string": b"",
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
        "scheme": "http",
    }
    return Request(scope)


def test_get_session_id_creates_cookie_when_missing():
    request = _make_request()
    response = Response()
    session_id = get_session_id(request, response)
    assert isinstance(session_id, uuid.UUID)
    set_cookie = response.headers.get("set-cookie", "")
    assert "session_id=" in set_cookie
    assert str(session_id) in set_cookie


def test_get_session_id_reuses_existing_cookie():
    existing_id = "50a3cbcd-0d4a-4c52-a804-a7a9286a454d"
    request = _make_request({"session_id": existing_id})
    response = Response()
    session_id = get_session_id(request, response)
    assert session_id == uuid.UUID(existing_id)
    assert response.headers.get("set-cookie") is None
