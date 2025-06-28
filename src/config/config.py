import os
from dotenv import load_dotenv

# Charger le .env à la racine
load_dotenv(override=True)

class Settings:
    NOMINATIM_URL = os.getenv("NOMINATIM_URL", "https://nominatim.openstreetmap.org/search")
    OPEN_METEO_URL = os.getenv("OPEN_METEO_URL", "https://api.open-meteo.com/v1/forecast")
    PORT = int(os.getenv("PORT", 3000))
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://weather_user:password@localhost:5432/weather_db')

settings = Settings()