from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.config.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(url=DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

async def init_db():
    from src.models.weather_model import WeatherData
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)