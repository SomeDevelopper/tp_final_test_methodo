import pytest
from testcontainers.postgres import PostgresContainer
from src.services.postgres_services import PostgresService
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from src.models.database import Base
from src.models.weather_model import HistoryWeather, ForecasWeather
import datetime


@pytest.mark.asyncio
async def test_postgres_service_current(monkeypatch):
    with PostgresContainer('postgres:15') as postgres:
        postgres_host_test = postgres.get_container_host_ip()
        postgres_port_test = postgres.get_exposed_port(postgres.port)
        postgres_username_test = postgres.username
        postgres_password_test = postgres.password
        postgres_dbname_test = postgres.dbname
        url_postgres_test = f"postgresql+asyncpg://{postgres_username_test}:{postgres_password_test}@{postgres_host_test}:{postgres_port_test}/{postgres_dbname_test}"
        engine = create_async_engine(url=url_postgres_test, echo=True, future=True)
        async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        monkeypatch.setattr("src.services.postgres_services.async_session", lambda: async_session())

        city = 'Paris'
        lat = 48.8566
        lon = 2.3522
        weather_data = {
            "temperature": 25.0,
            "windspeed": 12.0,
            "winddirection": 180,
            "time": datetime.datetime.utcnow().isoformat()
        }

        await PostgresService.save_weather(city=city, lat=lat, lon=lon, weather=weather_data)
        result = await PostgresService.get_weather(city=city)

        assert result is not None
        print(result)
        assert result.city == city.lower()
        assert result.temperature == 25.0

@pytest.mark.asyncio
async def test_postgres_service_forecast(monkeypatch):
    with PostgresContainer('postgres:15') as postgres:
        postgres_host_test = postgres.get_container_host_ip()
        postgres_port_test = postgres.get_exposed_port(postgres.port)
        postgres_username_test = postgres.username
        postgres_password_test = postgres.password
        postgres_dbname_test = postgres.dbname
        url_postgres_test = f"postgresql+asyncpg://{postgres_username_test}:{postgres_password_test}@{postgres_host_test}:{postgres_port_test}/{postgres_dbname_test}"
        engine = create_async_engine(url=url_postgres_test, echo=True, future=True)
        async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        monkeypatch.setattr("src.services.postgres_services.async_session", lambda: async_session())

        city = 'Paris'
        lat = 48.8566
        lon = 2.3522
        forecast = [
            ForecasWeather(date="2025-06-27", temperature_max=21.8, temperature_min=17.2),
            ForecasWeather(date="2025-06-28", temperature_max=26.7, temperature_min=14.9),
            ForecasWeather(date="2025-06-29", temperature_max=26.9, temperature_min=19.4),
            ForecasWeather(date="2025-06-30", temperature_max=26.8, temperature_min=13.6),
            ForecasWeather(date="2025-07-01", temperature_max=25.8, temperature_min=14.4)
        ]
        
        await PostgresService.save_forecast_weather(city=city, lat=lat, lon=lon, weather_forecast=forecast)
        result = await PostgresService.get_forecast_weather(city=city.lower())
        assert result is not None
        assert result.city == city.lower()
        assert result.latitude == lat
        assert result.longitude == lon
        assert len(result.forecast) == 5

@pytest.mark.asyncio
async def test_postgres_service_historical(monkeypatch):
    with PostgresContainer('postgres:15') as postgres:
        postgres_host_test = postgres.get_container_host_ip()
        postgres_port_test = postgres.get_exposed_port(postgres.port)
        postgres_username_test = postgres.username
        postgres_password_test = postgres.password
        postgres_dbname_test = postgres.dbname
        url_postgres_test = f"postgresql+asyncpg://{postgres_username_test}:{postgres_password_test}@{postgres_host_test}:{postgres_port_test}/{postgres_dbname_test}"
        engine = create_async_engine(url=url_postgres_test, echo=True, future=True)
        async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        monkeypatch.setattr("src.services.postgres_services.async_session", lambda: async_session())

        city = 'Paris'
        lat = 48.8566
        lon = 2.3522
        historical = [
            HistoryWeather(date="2025-06-22", temperature=33.1),
            HistoryWeather(date="2025-06-23", temperature=33.5),
            HistoryWeather(date="2025-06-24", temperature=34.8),
            HistoryWeather(date="2025-06-25", temperature=27.4),
            HistoryWeather(date="2025-06-26", temperature=24.9),
            HistoryWeather(date="2025-06-27", temperature=21.8)
        ]

        await PostgresService.save_history_weather(city=city, lat=lat, lon=lon, weather_history=historical)
        result = await PostgresService.get_history_weather(city=city.lower())
        assert result is not None
        assert result.city == city.lower()
        assert result.latitude == lat
        assert result.longitude == lon
        assert len(result.history) == 6