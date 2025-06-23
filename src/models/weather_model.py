from pydantic import BaseModel
from typing import List

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class CurrentWeather(BaseModel):
    temperature: float
    windspeed: float
    winddirection: float
    weathercode: int
    time: str

class ForecasWeather(BaseModel):
    date: str
    temperature_max: float
    temperature_min: float

class HistoryWeather(BaseModel):
    date: str
    temperature: float

class CurrentWeatherResponse(BaseModel):
    city: str
    coordinates: Coordinates
    current_weather: CurrentWeather

class ForecasWeatherResponse(BaseModel):
    city: str
    coordinates: Coordinates
    forecast: List[ForecasWeather]

class HistoryWeatherResponse(BaseModel):
    city: str
    coordinates: Coordinates
    history: List[HistoryWeather]
    