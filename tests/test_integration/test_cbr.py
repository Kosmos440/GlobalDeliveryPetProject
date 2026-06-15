from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.core.config import settings
from app.integration.cbr import get_usd_rate, get_usd_rate_from_cbr, api_url, CbrRateFetchError


@pytest.mark.asyncio
async def test_get_usd_rate_from_cbr():
    mock_response = MagicMock()
    mock_response.json.return_value = {"Valute": {"USD": {"Value": 92.5}}}

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    with patch("app.integration.cbr.httpx.AsyncClient", return_value=mock_client):
        rate = await get_usd_rate_from_cbr()

    assert rate == 92.5
    mock_client.get.assert_awaited_once_with(api_url)


@pytest.mark.asyncio
async def test_get_usd_rate_returns_cached_value():
    with patch("app.integration.cbr.cache_client") as mock_redis:
        mock_redis.get = AsyncMock(return_value=b"95.0")

        rate = await get_usd_rate()

    assert rate == 95.0
    mock_redis.get.assert_awaited_once_with("usd_rate")


@pytest.mark.asyncio
async def test_get_usd_rate_fetches_and_caches_on_miss():
    with (
        patch("app.integration.cbr.cache_client") as mock_redis,
        patch(
            "app.integration.cbr.get_usd_rate_from_cbr",
            new_callable=AsyncMock,
            return_value=90.0,
        ) as mock_cbr,
    ):
        mock_redis.get = AsyncMock(return_value=None)
        mock_redis.set = AsyncMock()

        rate = await get_usd_rate()

    assert rate == 90.0
    mock_cbr.assert_awaited_once()
    assert mock_redis.set.await_count == 2
    mock_redis.set.assert_any_await(
        "usd_rate",
        90.0,
        ex=settings.USD_RATE_CACHE_TTL,
    )
    mock_redis.set.assert_any_await("usd_rate_prev", 90.0)

@pytest.mark.asyncio
async def test_get_usd_rate_from_cbr_http_error():
    mock_client = AsyncMock()
    mock_client.get.side_effect = httpx.ConnectError("connection refused")
    mock_client.__aenter__.return_value = mock_client
    with patch("app.integration.cbr.httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(CbrRateFetchError):
            await get_usd_rate_from_cbr()

@pytest.mark.asyncio
async def test_get_usd_rate_uses_stale_on_cbr_failure():
    with (
        patch("app.integration.cbr.cache_client") as mock_redis,
        patch("app.integration.cbr.get_usd_rate_from_cbr", side_effect=CbrRateFetchError()),
    ):
        mock_redis.get = AsyncMock(side_effect=[None, b"88.0"])
        rate = await get_usd_rate()
    assert rate == 88.0
