import pytest
from src.services.geocoding_services import GeocodingService
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_get_coordinates(monkeypatch):
    class MockResponse:
        def json(self):
            return [{"lat": "48.86", "lon": "2.3199997"}]

    async def mock_get(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr('httpx.AsyncClient.get', mock_get)
    result_lat, result_lon = await GeocodingService.get_coordinates('Paris')
    assert result_lat == 48.86
    assert result_lon == 2.3199997

@pytest.mark.asyncio
async def test_get_coordinates_city_not_found(monkeypatch):
    class MockResponse:
        def json(self):
            return []  # Simule une réponse vide

    async def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_get)

    with pytest.raises(HTTPException) as exc_info:
        await GeocodingService.get_coordinates("VilleInventéeInconnue")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "City not found"