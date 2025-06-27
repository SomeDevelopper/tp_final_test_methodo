from fastapi import HTTPException
from src.config.config import settings
import httpx
import logging
from src.services.redis_services import RedisService
import json

logger = logging.getLogger(__name__)

class GeocodingService:
    NOMINATIM_URL = settings.NOMINATIM_URL

    @staticmethod
    async def get_coordinates(city: str, redis: RedisService):
        city = city.lower().strip()
        if '\x00' in city or not city.strip():
            raise HTTPException(status_code=400, detail="Invalid city input")
        redis_key = f"geo:{city}"

        cached = await redis.get(key=redis_key)
        if cached:
            lat, lon = json.loads(cached)
            return lat, lon
        params = {
            "q": city,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "WeatherAPI/1.0"
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    GeocodingService.NOMINATIM_URL,
                    params=params,
                    headers=headers,
                    timeout=10.0  # facultatif mais recommandé
                )
            except httpx.RequestError as e:
                logger.error(f"HTTP request error while getting coordinates for {city}: {e}")
                raise HTTPException(status_code=503, detail="Geocoding service unavailable")

            if response.status_code != 200:
                logger.error(f"Non-200 response from geocoding API for {city}: {response.status_code} - {response.text}")
                raise HTTPException(status_code=502, detail="Geocoding API error")

            try:
                data = response.json()
            except ValueError as e:
                logger.error(f"Failed to parse JSON for city '{city}': {e} - Raw content: {response.text}")
                raise HTTPException(status_code=502, detail="Invalid response from geocoding API")

            if not data:
                logger.warning(f"No coordinates found for city: {city}")
                raise HTTPException(status_code=404, detail=f"City '{city}' not found")

            try:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
            except (KeyError, ValueError, IndexError) as e:
                logger.error(f"Malformed geocoding data for {city}: {data}")
                raise HTTPException(status_code=500, detail="Geocoding data error")
            
            await redis.set(key=redis_key, value=json.dumps((lat, lon)), ttl=300)

            return lat, lon