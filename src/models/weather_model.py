from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, String, Float, DateTime, JSON
from src.models.database import Base
import datetime

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class CurrentWeather(BaseModel):
    temperature: float
    windspeed: float
    winddirection: float
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

class WeatherData(Base):
    __tablename__ = "weather_data"
    id = Column(String, primary_key=True)
    city = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    temperature = Column(Float)
    windspeed = Column(Float)
    winddirection = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class WeatherForcastData(Base):
    __tablename__ = "weather_forcast_data"
    id = Column(String, primary_key=True)
    city = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    forecast = Column(JSON)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow,  onupdate=datetime.datetime.utcnow)

class WeatherHistoryData(Base):
    __tablename__ = 'weather_history_data'
    id = Column(String, primary_key=True)
    city = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    history = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)