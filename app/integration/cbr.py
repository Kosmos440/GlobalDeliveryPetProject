import httpx
import structlog

from app.core.config import settings
from app.db.redis import cache_client
from app.exceptions.integration import (
    CbrRateBadResponseError,
    CbrRateFetchError,
    ExternalServiceException,
)

api_url = "https://www.cbr-xml-daily.ru/daily_json.js"
logger = structlog.get_logger(__name__)

async def get_usd_rate_from_cbr() -> float:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(api_url)
            response.raise_for_status()
            data = response.json()
            return float(data["Valute"]["USD"]["Value"])
    except httpx.TimeoutException as exc:
        logger.exception("cbr.timeout", url=api_url)
        raise CbrRateFetchError("CBR API request timed out") from exc
    except httpx.HTTPError as exc:
        logger.exception("cbr.http_error", url=api_url)
        raise CbrRateFetchError("CBR API returned an error or is unreachable") from exc
    except (KeyError, TypeError, ValueError) as exc:
        logger.exception("cbr.invalid_response", url=api_url)
        raise CbrRateBadResponseError("CBR API response format is invalid") from exc


async def get_usd_rate() -> float:
    cache = await cache_client.get("usd_rate")
    if cache:
        rate = float(cache.decode("utf-8"))
        logger.debug("cbr.rate_from_cache", rate=rate)
        return rate

    try:
        rate = await get_usd_rate_from_cbr()
    except ExternalServiceException:
        prev_rate = await cache_client.get("usd_rate_prev")
        if prev_rate:
            stale_rate = float(prev_rate.decode("utf-8"))
            logger.warning("cbr.using_stale_rate", rate=stale_rate)
            return stale_rate
        raise

    await cache_client.set("usd_rate", rate, ex=settings.USD_RATE_CACHE_TTL)
    await cache_client.set("usd_rate_prev", rate)
    logger.info("cbr.rate_cached", rate=rate)

    return rate
