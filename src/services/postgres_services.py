from sqlalchemy import select
from models.database import async_session
from models.weather_model import WeatherData, WeatherForcastData, WeatherHistoryData
import datetime

class PostgresService:
    @staticmethod
    async def get_weather(city: str):
        async with async_session() as session:
            result = await session.execute(
                select(WeatherData).where(WeatherData.city==city.lower())
            )
            weather = result.scalar_one_or_none()
            return weather
        
    @staticmethod
    async def save_weather(city: str, lat: float, lon: float, weather: dict):
        async with async_session() as session:
            if isinstance(weather.get('time'), str):
                weather['time'] = datetime.datetime.fromisoformat(weather.get('time'))
            weather_city = WeatherData(
                id=f"{city}-{weather.get('time')}",
                city=city.lower(),
                latitude=lat,
                longitude=lon,
                temperature=weather.get("temperature"),
                windspeed=weather.get('windspeed'),
                winddirection=weather.get('winddirection'),
                timestamp=weather.get('time')
            )
            session.add(weather_city)
            await session.commit()

    @staticmethod
    async def get_forecast_weather(city: str):
        async with async_session() as session:
            result = await session.execute(
                select(WeatherForcastData).where(WeatherForcastData.city==city.lower())
            )
            weather_forecast = result.scalar_one_or_none()
            return weather_forecast
        
    @staticmethod
    async def save_forecast_weather(city: str, lat: float, lon: float, weather_forecast: list):
        forecast_dict = [item.dict() for item in weather_forecast]
        async with async_session() as session:
            weather_forecast_city = WeatherForcastData(
                id=f"{city}",
                city=city.lower(),
                latitude=lat,
                longitude=lon,
                forecast=forecast_dict
            )
            session.add(weather_forecast_city)
            await session.commit()

    @staticmethod
    async def get_history_weather(city: str):
        async with async_session() as session:
            result = await session.execute(
                select(WeatherHistoryData).where(WeatherHistoryData.city==city.lower())
            )
            weather_history = result.scalar_one_or_none()
            return weather_history

    @staticmethod
    async def save_history_weather(city: str, lat: float, lon: float, weather_history: list):
        history_dict = [item.dict() for item in weather_history]
        async with async_session() as session:
            weather_history_city = WeatherHistoryData(
                id=f"{city}",
                city=city.lower(),
                latitude=lat,
                longitude=lon,
                history=history_dict
            )
            session.add(weather_history_city)
            await session.commit()