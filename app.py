from fastapi import FastAPI
from src.controllers import weather_controller, healther_controller
from src.config.config import settings
from contextlib import asynccontextmanager
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator
from src.models.database import init_db


app = FastAPI()

Instrumentator().instrument(app).expose(app)

app.include_router(weather_controller.router)
app.include_router(healther_controller.router)

@app.on_event('startup')
async def startup_event():
    await init_db()



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=settings.PORT)