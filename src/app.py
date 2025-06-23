from fastapi import FastAPI
from controllers import weather_controller, healther_controller
from config.config import settings
import uvicorn

app = FastAPI()

app.include_router(weather_controller.router)
app.include_router(healther_controller.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=settings.PORT)