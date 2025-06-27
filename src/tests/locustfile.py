from locust import HttpUser, between, task
import random

class UserTest(HttpUser):
    wait_time = between(0.5, 2)
    city_list = ['Paris', 'Rome', 'Madrid', 'New York', 'Tokyo', 'Berlin', 'Londres']

    @task(5)
    def current_weather_get(self):
        city = random.choice(self.city_list)
        with self.client.get(f'/weather/current/{city}', catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get current weather for {city}")
            else:
                response.success()
    
    @task(2)
    def forecast_weather_get(self):
        city = random.choice(self.city_list)
        with self.client.get(f'/weather/forecast/{city}', catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Forecast weather failed for {city}")

    @task(1)
    def history_weather_get(self):
        city = random.choice(self.city_list)
        with self.client.get(f'/weather/history/{city}', catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"History weather failed for {city}")

    @task(1)
    def health_check(self):
        with self.client.get('/health', catch_response=True) as response:
            if response.status_code != 200 or response.json().get("status") != "ok":
                response.failure("Health check failed")
            else:
                response.success()