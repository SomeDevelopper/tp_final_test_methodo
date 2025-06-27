from fastapi import APIRouter
from src.services.geocoding_services import GeocodingService
from src.services.weather_services import WeatherService
from src.models.weather_model import (
    CurrentWeather, CurrentWeatherResponse, Coordinates,
    ForecasWeather, ForecasWeatherResponse,
    HistoryWeather, HistoryWeatherResponse
)
from src.services.redis_services import RedisService
from src.services.postgres_services import PostgresService

router = APIRouter(prefix='/weather', tags=['Weather'])
redis_service = RedisService()

@router.get("/current/{city}", response_model=CurrentWeatherResponse, responses={
    502: {"description": "Geocoding API error"},
    404: {"description": "City {city} not found"}})
async def get_current_weather(city: str):
    cache_key = f"weather:current:{city.lower()}"

    cache_data = await redis_service.get(key=cache_key)
    if cache_data:
        return CurrentWeatherResponse.parse_raw(cache_data)
    
    db_data = await PostgresService.get_weather(city=city)
    if db_data:
        response = CurrentWeatherResponse(
            city=city,
            coordinates=Coordinates(latitude=db_data.latitude, longitude=db_data.longitude),
            current_weather=CurrentWeather(
            temperature=db_data.temperature,
            windspeed=db_data.windspeed,
            winddirection=db_data.winddirection,
            time=db_data.timestamp.isoformat()
            )
        )
        await redis_service.set(cache_key, response.json(), ttl=300)
        print("Une donnée a été ajoutée")
        return response

    lat, lon = await GeocodingService.get_coordinates(city=city, redis=redis_service)

    weather_data = await WeatherService.get_current_weather(lat=lat, lon=lon)

    if weather_data == "Error":
        return {'status': 200, 'response': 'Aucune donnée trouvé'}

    current = weather_data.get("current_weather", {})

    current_weather_response = CurrentWeatherResponse(
        city=city,
        coordinates=Coordinates(latitude=lat, longitude=lon),
        current_weather=CurrentWeather(
            temperature=current.get("temperature"),
            windspeed=current.get("windspeed"),
            winddirection=current.get("winddirection"),
            time=current.get("time")
        )
    )

    await redis_service.set(cache_key, current_weather_response.json(), ttl=300)
    await PostgresService.save_weather(city=city, lat=lat, lon=lon, weather=current)
    print("Une donnée a été ajoutée")
    return current_weather_response


@router.get('/forecast/{city}', response_model=ForecasWeatherResponse, responses={
    502: {"description": "Geocoding API error"},
    404: {"description": "City {city} not found"}})
async def get_forecast_weather(city: str):
    
    cache_key = f"weather:forecast:{city.lower()}"
    cache_data = await redis_service.get(key=cache_key)
    if cache_data:
        return ForecasWeatherResponse.parse_raw(cache_data)
    
    forecast_db = await PostgresService.get_forecast_weather(city=city.lower())
    if forecast_db:
        response = ForecasWeatherResponse(
            city=city,
            coordinates=Coordinates(latitude=forecast_db.latitude, longitude=forecast_db.longitude),
            forecast=forecast_db.forecast
        )
        await redis_service.set(key=cache_key, value=response.json(), ttl=300)
        print('Une donnée à été ajoutée')
        return response
    
    lat, lon = await GeocodingService.get_coordinates(city=city, redis=redis_service)

    weather_data = await WeatherService.get_forecast_weather(lat=lat, lon=lon)

    forecast = [ForecasWeather(date=date, temperature_max=t_max, temperature_min=t_min) 
                 for date, t_max, t_min in zip(
                    weather_data["daily"]["time"],
                    weather_data["daily"]["temperature_2m_max"],
                    weather_data["daily"]["temperature_2m_min"]
                 )]
    
    forecast_weather_response = ForecasWeatherResponse(
        city=city,
        coordinates=Coordinates(latitude=lat, longitude=lon),
        forecast=forecast
    )
    await redis_service.set(key=cache_key, value=forecast_weather_response.json(), ttl=300)
    await PostgresService.save_forecast_weather(city=city, lat=lat, lon=lon, weather_forecast=forecast)
    print("Des données ont été ajoutées")
    return forecast_weather_response

@router.get("/history/{city}", response_model=HistoryWeatherResponse, responses={
    502: {"description": "Geocoding API error"},
    404: {"description": "City {city} not found"}})
async def get_history_weather(city: str):
    cache_key = f"weather:history:{city.lower()}"
    cache_data = await redis_service.get(key=cache_key)
    if cache_data:
        return HistoryWeatherResponse.parse_raw(cache_data)
    
    history_data = await PostgresService.get_history_weather(city=city)
    if history_data:
        response = HistoryWeatherResponse(
            city=city,
            coordinates=Coordinates(latitude=history_data.latitude, longitude=history_data.longitude),
            history=history_data.history
        )
        await redis_service.set(key=cache_key, value=response.json(), ttl=300)
        print('Une donnée à été ajoutée')
        return response

    lat, lon = await GeocodingService.get_coordinates(city=city, redis=redis_service)

    weather_data = await WeatherService.get_historical_weather(lat, lon)

    history = [HistoryWeather(date=date, temperature=temp) 
               for date, temp in zip(
                    weather_data["daily"]["time"],
                    weather_data["daily"]["temperature_2m_max"]
               )]

    history_weather_response = HistoryWeatherResponse(
        city=city,
        coordinates=Coordinates(latitude=lat, longitude=lon),
        history=history
    )

    await redis_service.set(key=cache_key, value=history_weather_response.json(), ttl=300)
    await PostgresService.save_history_weather(city=city, lat=lat, lon=lon, weather_history=history)
    print('Des données ont été ajoutées')
    return history_weather_response