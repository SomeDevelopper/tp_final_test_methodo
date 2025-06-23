from fastapi import HTTPException
from config.config import settings
import httpx

class GeocodingService:
    NOMINATIM_URL = settings.NOMINATIM_URL

    @staticmethod
    async def get_coordinates(city: str):
        params = {
            "q": city,
            "format": "json",
            "limit": 1
        }

        header = {
            "User-Agent": "WeatherAPI/1.0"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(GeocodingService.NOMINATIM_URL, params=params, headers=header)
            data = response.json()
        
        if not data:
            raise HTTPException(status_code=404, detail="City not found")
        
        lat = float(data[0]["lat"])
        lon = float(data[0]['lon'])
        return lat, lon