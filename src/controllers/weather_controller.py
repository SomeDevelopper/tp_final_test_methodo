from fastapi import APIRouter
from services.geocoding_services import GeocodingService
from services.weather_services import WeatherService
from models.weather_model import (
    CurrentWeather, CurrentWeatherResponse, Coordinates,
    ForecasWeather, ForecasWeatherResponse,
    HistoryWeather, HistoryWeatherResponse
)
from services.redis_services import RedisService

router = APIRouter(prefix='/weather', tags=['Weather'])
redis_service = RedisService()

@router.get("/current/{city}", response_model=CurrentWeatherResponse)
async def get_current_weather(city: str):
    lat, lon = await GeocodingService.get_coordinates(city=city)
    cache_key = f"weather:current:{city.lower()}"

    cache_data = await redis_service.get(key=cache_key)
    if cache_data:
        return CurrentWeatherResponse.parse_raw(cache_data)
    weather_data = await WeatherService.get_current_weather(lat=lat, lon=lon)

    current = weather_data.get("current_weather", {})


    current_weather_response = CurrentWeatherResponse(
        city=city,
        coordinates=Coordinates(latitude=lat, longitude=lon),
        current_weather=CurrentWeather(
            temperature=current.get("temperature"),
            windspeed=current.get("windspeed"),
            winddirection=current.get("winddirection"),
            weathercode=current.get("weathercode"),
            time=current.get("time")
        )
    )

    await redis_service.set(cache_key, current_weather_response.json(), ttl=300)
    print("Une donnée a été ajoutée")
    return current_weather_response


@router.get('/forecast/{city}', response_model=ForecasWeatherResponse)
async def get_forecast_weather(city: str):
    lat, lon = await GeocodingService.get_coordinates(city=city)
    cache_key = f"weather:forecast:{city.lower()}"
    cache_data = await redis_service.get(key=cache_key)
    if cache_data:
        return ForecasWeatherResponse.parse_raw(cache_data)

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
    print("Des données ont été ajoutées")
    return forecast_weather_response

@router.get("/history/{city}", response_model=HistoryWeatherResponse)
async def get_history_weather(city: str):
    lat, lon = await GeocodingService.get_coordinates(city)
    cache_key = f"weather:history:{city.lower()}"
    cache_data = await redis_service.get(key=cache_key)
    if cache_data:
        return HistoryWeatherResponse.parse_raw(cache_data)

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
    print('Des données ont été ajoutées')
    return history_weather_response