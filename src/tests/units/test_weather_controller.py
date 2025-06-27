import pytest
from src.controllers.weather_controller import get_current_weather, get_forecast_weather, get_history_weather
from unittest.mock import AsyncMock
from src.services.geocoding_services import GeocodingService
from src.services.postgres_services import PostgresService
from src.services.weather_services import WeatherService
from src.services.redis_services import RedisService

@pytest.mark.asyncio
async def test_get_current_weather_controller(monkeypatch):
    city = "Paris"
    lat, lon = 48.8566, 2.3522
    fake_weather = {
        "temperature": 22.5,
        "windspeed": 10.0,
        "winddirection": 180,
        "time": "2024-06-27T10:00:00"
    }
    monkeypatch.setattr(GeocodingService, "get_coordinates", AsyncMock(return_value=(lat, lon)))
    monkeypatch.setattr(RedisService, "get", AsyncMock(return_value=None))
    monkeypatch.setattr(PostgresService, "get_weather", AsyncMock(return_value=None))
    monkeypatch.setattr(WeatherService, "get_current_weather", AsyncMock(return_value={"current_weather": fake_weather}))
    monkeypatch.setattr(RedisService, "set", AsyncMock())
    monkeypatch.setattr(PostgresService, "save_weather", AsyncMock())

    result = await get_current_weather(city)

    assert result.city == city
    assert result.coordinates.latitude == lat
    assert result.current_weather.temperature == fake_weather["temperature"]

@pytest.mark.asyncio
async def test_get_forecast_weather_controller(monkeypatch):
    city = "Paris"
    lat, lon = 48.8566, 2.3522
    fake_forecast = {
        "daily": {
            "time": ["2024-06-28", "2024-06-29"],
            "temperature_2m_max": [30, 32],
            "temperature_2m_min": [18, 19]
        }
    }

    monkeypatch.setattr(RedisService, "get", AsyncMock(return_value=None))
    monkeypatch.setattr(PostgresService, "get_forecast_weather", AsyncMock(return_value=None))
    monkeypatch.setattr(GeocodingService, "get_coordinates", AsyncMock(return_value=(lat, lon)))
    monkeypatch.setattr(WeatherService, "get_forecast_weather", AsyncMock(return_value=fake_forecast))
    monkeypatch.setattr(PostgresService, "save_forecast_weather", AsyncMock())
    monkeypatch.setattr(RedisService, "set", AsyncMock())

    response = await get_forecast_weather(city)

    assert response.city == city
    assert len(response.forecast) == 2
    assert response.forecast[0].temperature_max == 30

@pytest.mark.asyncio
async def test_get_historical_weather_controller(monkeypatch):
    city = "Paris"
    lat, lon = 48.8566, 2.3522
    fake_history = {
        "daily": {
            "time": ["2024-06-25", "2024-06-26"],
            "temperature_2m_max": [29, 31]
        }
    }

    monkeypatch.setattr(RedisService, "get", AsyncMock(return_value=None))
    monkeypatch.setattr(PostgresService, "get_history_weather", AsyncMock(return_value=None))
    monkeypatch.setattr(GeocodingService, "get_coordinates", AsyncMock(return_value=(lat, lon)))
    monkeypatch.setattr(WeatherService, "get_historical_weather", AsyncMock(return_value=fake_history))
    monkeypatch.setattr(PostgresService, "save_history_weather", AsyncMock())
    monkeypatch.setattr(RedisService, "set", AsyncMock())

    response = await get_history_weather(city)

    assert response.city == city
    assert len(response.history) == 2
    assert response.history[0].temperature == 29