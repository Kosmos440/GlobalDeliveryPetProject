import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from app.api.v1.routers.package import package_router
from app.api.v1.routers.package_categories import package_categories_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.logging_context import LoggingContextMiddleware

setup_logging()
app = FastAPI(title="Global Delivery")
main_api_router = APIRouter()

main_api_router.include_router(package_router, prefix=f"{settings.API_PREFIX}/package", tags=["package"])
main_api_router.include_router(package_categories_router, prefix=f"{settings.API_PREFIX}/categories", tags=["categories"])
app.include_router(main_api_router)
app.add_middleware(LoggingContextMiddleware)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
