import uuid

from starlette.responses import Response

from app.core.session_manager import get_session_id


def test_get_session_id_creates_cookie_when_missing():
    response = Response()
    session_id = get_session_id(response=response, session_id=None)
    assert isinstance(session_id, uuid.UUID)
    set_cookie = response.headers.get("set-cookie", "")
    assert "session_id=" in set_cookie
    assert str(session_id) in set_cookie


def test_get_session_id_reuses_existing_cookie():
    existing_id = "50a3cbcd-0d4a-4c52-a804-a7a9286a454d"
    response = Response()
    session_id = get_session_id(response=response, session_id=existing_id)
    assert session_id == uuid.UUID(existing_id)
    assert response.headers.get("set-cookie") is None


def test_get_session_id_recreates_cookie_when_invalid():
    response = Response()
    session_id = get_session_id(response=response, session_id="not-a-uuid")
    assert isinstance(session_id, uuid.UUID)
    set_cookie = response.headers.get("set-cookie", "")
    assert "session_id=" in set_cookie
    assert str(session_id) in set_cookie
