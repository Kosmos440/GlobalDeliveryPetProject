from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"

    )

    # Приложение
    APP_NAME: str = "Global Delivery"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool
    API_PREFIX: str = "/api/v1"

    # PostgreSQL
    POSTGRES_PORT: int = 5434
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DATABASE_URL: str | None = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v: Any, info) -> Any:
        if v:
            return v
        data = info.data
        return (
            f"postgresql+asyncpg://{data['POSTGRES_USER']}:{data['POSTGRES_PASSWORD']}"
            f"@{data['POSTGRES_HOST']}:{data['POSTGRES_PORT']}/{data['POSTGRES_DB']}"
        )

    # Redis
    REDIS_PORT: int = 6379
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_BROKER_PREFIX: int = 0
    REDIS_CACHE_PREFIX: int = 1

    REDIS_BROKER: str | None = None
    REDIS_CACHE: str | None = None

    @field_validator("REDIS_BROKER", mode="before")
    @classmethod
    def assemble_redis_broker(cls, v: Any, info) -> Any:
        if v:
            return v
        data = info.data
        return (
            f"redis://:{data['REDIS_PASSWORD']}"
            f"@{data['REDIS_HOST']}:{data['REDIS_PORT']}/{data['REDIS_BROKER_PREFIX']}"
        )

    @field_validator("REDIS_CACHE", mode="before")
    @classmethod
    def assemble_redis_cache(cls, v: Any, info) -> Any:
        if v:
            return v
        data = info.data
        return (
            f"redis://:{data['REDIS_PASSWORD']}"
            f"@{data['REDIS_HOST']}:{data['REDIS_PORT']}/{data['REDIS_CACHE_PREFIX']}"
        )

    # Кеш
    USD_RATE_CACHE_TTL: int = 600

settings = Settings()
