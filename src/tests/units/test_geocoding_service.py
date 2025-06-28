import pytest
from src.services.geocoding_services import GeocodingService
from fastapi import HTTPException
from unittest.mock import AsyncMock
from src.services.redis_services import RedisService
import httpx

mock_redis = AsyncMock(spec=RedisService)
mock_redis.get.return_value = None
mock_redis.set.return_value = None

@pytest.mark.asyncio
async def test_get_coordinates(monkeypatch):
    class MockResponse:
        status_code = 200
        def json(self):
            return [{"lat": "48.86", "lon": "2.3199997"}]

    async def mock_get(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr('httpx.AsyncClient.get', mock_get)
    result_lat, result_lon = await GeocodingService.get_coordinates('Paris', redis=mock_redis)
    assert result_lat == 48.86
    assert result_lon == 2.3199997

@pytest.mark.asyncio
async def test_city_found_in_cache():
    mock_redis.get.return_value = '[48.86, 2.3199997]'

    result_lat, result_lon = await GeocodingService.get_coordinates("Paris", redis=mock_redis)
    assert result_lat == 48.86
    assert result_lon == 2.3199997

@pytest.mark.asyncio
async def test_invalid_city_input():
    with pytest.raises(HTTPException) as exc_info:
        await GeocodingService.get_coordinates(" \x00 ", redis=mock_redis)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid city input"

@pytest.mark.asyncio
async def test_get_coordinates_city_not_found(monkeypatch):
    mock_redis.get.return_value = None
    class MockResponse:
        status_code = 200
        text = "City 'VilleInventéeInconnue' not found"
        def json(self):
            return []  # Simule une réponse vide

    async def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    with pytest.raises(HTTPException) as exc_info:
        await GeocodingService.get_coordinates("VilleInventéeInconnue", redis=mock_redis)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "City 'villeinventéeinconnue' not found"

@pytest.mark.asyncio
async def test_http_status_not_200(monkeypatch):
    mock_redis.get.return_value = None

    class MockResponse:
        status_code = 502
        text = "Bad Gateway"
        def json(self):
            return {}

    async def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    with pytest.raises(HTTPException) as exc_info:
        await GeocodingService.get_coordinates("Paris", redis=mock_redis)

    assert exc_info.value.status_code == 502
    assert exc_info.value.detail == "Geocoding API error"


@pytest.mark.asyncio
async def test_invalid_json(monkeypatch):
    mock_redis.get.return_value = None

    class MockResponse:
        status_code = 200
        text = "Not JSON"
        def json(self):
            raise ValueError("Invalid JSON")

    async def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    with pytest.raises(HTTPException) as exc_info:
        await GeocodingService.get_coordinates("Paris", redis=mock_redis)

    assert exc_info.value.status_code == 502
    assert exc_info.value.detail == "Invalid response from geocoding API"


@pytest.mark.asyncio
async def test_malformed_data(monkeypatch):
    mock_redis.get.return_value = None

    class MockResponse:
        status_code = 200
        text = '[{"bad": "data"}]'
        def json(self):
            return [{"bad": "data"}]

    async def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    with pytest.raises(HTTPException) as exc_info:
        await GeocodingService.get_coordinates("Paris", redis=mock_redis)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Geocoding data error"


@pytest.mark.asyncio
async def test_httpx_request_error(monkeypatch):
    mock_redis.get.return_value = None

    class MockClient:
        async def get(self, *args, **kwargs):
            raise httpx.RequestError("Timeout", request=None)

        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            pass

    monkeypatch.setattr("httpx.AsyncClient", lambda: MockClient())

    with pytest.raises(HTTPException) as exc_info:
        await GeocodingService.get_coordinates("Paris", redis=mock_redis)

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Geocoding service unavailable"