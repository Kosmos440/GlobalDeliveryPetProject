import uuid

import structlog
from fastapi import Cookie, Response

logger = structlog.get_logger(__name__)

SESSION_ID_COOKIE = Cookie(
    default=None,
    description=(
        "Идентификатор сессии пользователя. "
        "Если cookie отсутствует или содержит невалидный UUID, сервер создаёт новую сессию "
        "и возвращает cookie в ответе."
    ),
)


def get_session_id(
    response: Response,
    session_id: str | None = SESSION_ID_COOKIE,
) -> uuid.UUID:
    if not session_id:
        new_session_id = uuid.uuid4()
        response.set_cookie("session_id", str(new_session_id))
        logger.debug("session.created", session_id=str(new_session_id), reason="missing_cookie")
        return new_session_id

    try:
        parsed_session_id = uuid.UUID(session_id)
        logger.debug("session.found", session_id=str(parsed_session_id))
        return parsed_session_id
    except ValueError:
        new_session_id = uuid.uuid4()
        response.set_cookie("session_id", str(new_session_id))
        logger.info("session.created", session_id=str(new_session_id), reason="invalid_cookie")
        return new_session_id
