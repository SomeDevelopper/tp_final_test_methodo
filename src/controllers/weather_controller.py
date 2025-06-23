from fastapi import APIRouter
from services.geocoding_services import GeocodingService
from services.weather_services import WeatherService
from models.weather_model import (
    CurrentWeather, CurrentWeatherResponse, Coordinates,
    ForecasWeather, ForecasWeatherResponse,
    HistoryWeather, HistoryWeatherResponse
)

router = APIRouter(prefix='/weather', tags=['Weather'])

@router.get("/current/{city}", response_model=CurrentWeatherResponse)
async def get_current_weather(city: str):
    lat, lon = await GeocodingService.get_coordinates(city=city)
    weather_data = await WeatherService.get_current_weather(lat=lat, lon=lon)

    current = weather_data.get("current_weather", {})

    return CurrentWeatherResponse(
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


@router.get('/forecast/{city}', response_model=ForecasWeatherResponse)
async def get_forecast_weather(city: str):
    lat, lon = await GeocodingService.get_coordinates(city=city)
    weather_data = await WeatherService.get_forecast_weather(lat=lat, lon=lon)
    print(weather_data)

    forecast = [ForecasWeather(date=date, temperature_max=t_max, temperature_min=t_min) 
                 for date, t_max, t_min in zip(
                    weather_data["daily"]["time"],
                    weather_data["daily"]["temperature_2m_max"],
                    weather_data["daily"]["temperature_2m_min"]
                 )]
    
    return ForecasWeatherResponse(
        city=city,
        coordinates=Coordinates(latitude=lat, longitude=lon),
        forecast=forecast
    )

@router.get("/history/{city}", response_model=HistoryWeatherResponse)
async def get_history_weather(city: str):
    lat, lon = await GeocodingService.get_coordinates(city)
    weather_data = await WeatherService.get_historical_weather(lat, lon)

    history = []
    for date, temp in zip(
        weather_data["daily"]["time"],
        weather_data["daily"]["temperature_2m_max"]
    ):
        history.append(HistoryWeather(
            date=date,
            temperature=temp
        ))

    return HistoryWeatherResponse(
        city=city,
        coordinates=Coordinates(latitude=lat, longitude=lon),
        history=history
    )