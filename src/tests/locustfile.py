from locust import HttpUser, between, task
import random

class UserTest(HttpUser):

    @task
    def current_weather_get_test(self):
        city_list = ['Paris', 'Rome', 'Madrid', 'New York', 'Tokyo', 'Berlin', 'Londre']
        city = city_list[random.randint(0, len(city_list) - 1)]
        self.client.get(f'/weather/current/{city}')

    @task
    def health_api_test(self):
        response = self.client.get(f'/health').json()
        assert response['status'] == 'ok'