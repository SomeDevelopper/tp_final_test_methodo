import os
from dotenv import load_dotenv

# Charger le .env à la racine
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env'))

class Settings:
    NOMINATIM_URL = os.environ.get("NOMINATIM_URL", "https://nominatim.openstreetmap.org/search")
    OPEN_METEO_URL = os.environ.get("OPEN_METEO_URL", "https://api.open-meteo.com/v1/forecast")
    PORT = int(os.environ.get("PORT", 3000))
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")

settings = Settings()