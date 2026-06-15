import uuid

import structlog
from fastapi import Request, Response

logger = structlog.get_logger(__name__)


def get_session_id(request: Request, response: Response) -> uuid.UUID:
    session_id = request.cookies.get("session_id")

    if not session_id:
        session_id = uuid.uuid4()
        response.set_cookie("session_id", str(session_id))
        logger.debug("session.created", session_id=str(session_id), reason="missing_cookie")
    else:
        try:
            session_id = uuid.UUID(session_id)
            logger.debug("session.found", session_id=str(session_id))
        except ValueError:
            session_id = uuid.uuid4()
            response.set_cookie("session_id", str(session_id))
            logger.info("session.created", session_id=str(session_id), reason="invalid_cookie")

    return session_id
