import pytest
from src.services.weather_services import WeatherService
from src.models.weather_model import ForecasWeather, HistoryWeather

@pytest.mark.asyncio
async def test_get_current_weather(monkeypatch):
    class MockResponseCurrent:
        def json(self):
            return {'latitude': 48.86, 
                    'longitude': 2.3199997, 
                    'generationtime_ms': 0.052094459533691406, 
                    'utc_offset_seconds': 0, 
                    'timezone': 'GMT', 
                    'timezone_abbreviation': 'GMT', 
                    'elevation': 38.0, 
                    'current_weather_units': {
                        'time': 'iso8601', 
                        'interval': 'seconds', 
                        'temperature': '°C', 
                        'windspeed': 'km/h', 
                        'winddirection': '°', 
                        'is_day': '', 
                        'weathercode': 'wmo code'}, 
                        'current_weather': {
                            'time': '2025-06-27T09:15', 
                            'interval': 900, 
                            'temperature': 23.1, 
                            'windspeed': 10.7, 
                            'winddirection': 256, 
                            'is_day': 1, 
                            'weathercode': 2}
                    }
    async def mock_get_current(*args, **kwargs):
        return MockResponseCurrent()
    monkeypatch.setattr('httpx.AsyncClient.get', mock_get_current)
    result = await WeatherService.get_current_weather(lat=48.86, lon=2.3199997)
    current = result.get("current_weather", {})
    assert result.get('latitude') == 48.86
    assert result.get('longitude') == 2.3199997
    assert current.get("temperature")
    assert current.get("windspeed")
    assert current.get("winddirection")
    assert current.get("weathercode")
    assert current.get("time")


@pytest.mark.asyncio
async def test_get_forecast_weather(monkeypatch):
    class MockReponseForecast():
        def json(self):
            return {'latitude': 48.86, 
                'longitude': 2.3199997, 
                'generationtime_ms': 0.03707408905029297, 
                'utc_offset_seconds': 7200, 
                'timezone': 'Europe/Paris', 
                'timezone_abbreviation': 'GMT+2', 
                'elevation': 43.0, 
                'daily_units': {
                    'time': 'iso8601', 
                    'temperature_2m_max': '°C', 
                    'temperature_2m_min': '°C'}, 
                    'daily': {
                        'time': ['2025-06-27', '2025-06-28', '2025-06-29', '2025-06-30', '2025-07-01'], 
                        'temperature_2m_max': [28.1, 31.0, 31.0, 35.0, 38.1], 
                        'temperature_2m_min': [20.6, 21.2, 19.9, 20.1, 22.6]
                    }
                }
    async def mock_get_forecast(*args, **kwargs):
        return MockReponseForecast()
    monkeypatch.setattr('httpx.AsyncClient.get', mock_get_forecast)
    result = await WeatherService.get_forecast_weather(lat=48.86, lon=2.3199997)
    forecast = [ForecasWeather(date=date, temperature_max=t_max, temperature_min=t_min) 
                 for date, t_max, t_min in zip(
                    result["daily"]["time"],
                    result["daily"]["temperature_2m_max"],
                    result["daily"]["temperature_2m_min"]
                )]
    assert result.get('latitude') == 48.86
    assert result.get('longitude') == 2.3199997
    assert len(forecast) == 5

@pytest.mark.asyncio
async def test_get_historical_weather(monkeypatch):
    class MockResponseHistorical():
        def json(self):
            return {'latitude': 41.875, 
                'longitude': 12.5, 
                'generationtime_ms': 0.02181529998779297, 
                'utc_offset_seconds': 7200, 
                'timezone': 'Europe/Rome', 
                'timezone_abbreviation': 'GMT+2', 
                'elevation': 42.0, 
                'daily_units': {
                    'time': 'iso8601', 
                    'temperature_2m_max': '°C'
                    }, 
                'daily': {
                    'time': ['2025-06-22', '2025-06-23', '2025-06-24', '2025-06-25', '2025-06-26', '2025-06-27'], 
                    'temperature_2m_max': [33.1, 33.5, 32.8, 33.4, 34.5, 35.8]}}
    async def mock_get_history(*args, **kwargs):
        return MockResponseHistorical()
    monkeypatch.setattr('httpx.AsyncClient.get', mock_get_history)
    result = await WeatherService.get_historical_weather(lat=41.875, lon=12.5)
    history = [HistoryWeather(date=date, temperature=temp) 
               for date, temp in zip(
                    result["daily"]["time"],
                    result["daily"]["temperature_2m_max"]
               )]
    assert result.get('latitude') == 41.875
    assert result.get('longitude') == 12.5
    assert len(history) == 6