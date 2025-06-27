import httpx
from fastapi import HTTPException
from src.config.config import settings

class WeatherService:
    OPEN_METEO_URL = settings.OPEN_METEO_URL

    @staticmethod
    async def get_current_weather(lat: float, lon: float):
        params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': 'true'
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(WeatherService.OPEN_METEO_URL, params=params)
            data = response.json()

        return data
    
    @staticmethod
    async def get_forecast_weather(lat: float, lon: float):
        params = [
            ("latitude", lat),
            ("longitude", lon),
            ("forecast_days", 5),
            ("timezone", "auto"),
            ("daily", "temperature_2m_max"),
            ("daily", "temperature_2m_min")
        ]

        async with httpx.AsyncClient() as client:
            response = await client.get(WeatherService.OPEN_METEO_URL, params=params)
            data = response.json()

            if "daily" not in data:
                raise HTTPException(status_code=500, detail="No daily forecast data returned")
            
        return data

        
    @staticmethod
    async def get_historical_weather(lat: float, lon: float):
        from datetime import date, timedelta

        end_date = date.today()
        start_date = end_date - timedelta(days=5)

        params = {
            'latitude': lat,
            'longitude': lon,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'daily': 'temperature_2m_max',
            'timezone': 'auto'
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(WeatherService.OPEN_METEO_URL, params=params)
            data = response.json()
        return data