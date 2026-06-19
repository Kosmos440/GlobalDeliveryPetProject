from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from starlette.staticfiles import StaticFiles

from app.api.v1.routers.package import package_router
from app.api.v1.routers.package_categories import package_categories_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.logging_context import LoggingContextMiddleware
from app.exceptions.handlers import register_exception_handlers

setup_logging()
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    openapi_tags=[
        {"name": "package", "description": "Создание и просмотр посылок"},
        {"name": "categories", "description": "Справочник категорий посылок"},
    ],
)
main_api_router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

main_api_router.include_router(package_router, prefix=f"{settings.API_PREFIX}/package", tags=["package"])
main_api_router.include_router(package_categories_router, prefix=f"{settings.API_PREFIX}/categories", tags=["categories"])
app.include_router(main_api_router)
app.add_middleware(LoggingContextMiddleware)
app.mount("/ui", StaticFiles(directory=FRONTEND_DIR, html=True), name="ui")
register_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
