from src.services.redis_services import RedisService
import pytest
from testcontainers.redis import RedisContainer

@pytest.mark.asyncio
async def test_redis_service(monkeypatch):
    with RedisContainer('redis:5.0.3-alpine') as redis_serveur_test:
        redis_host_ip_test = redis_serveur_test.get_container_host_ip()
        redis_port_test = redis_serveur_test.get_exposed_port('6379')
        redis_url_test = f"redis://{redis_host_ip_test}:{redis_port_test}"
        redis_handler = RedisService(redis_url=redis_url_test)
        test_redis_key = "current_weather_key_paris"
        test_redis_value = {
            'latitude': 48.86, 
            'longitude': 2.3199997,
            'city': 'Paris',
            'temperature': 23.1, 
            'windspeed': 10.7, 
            'winddirection': 256
        }
        await redis_handler.set(key=test_redis_key, value=test_redis_value, ttl=300)
        redis_cache_data = await redis_handler.get(key=test_redis_key)
        assert redis_cache_data == test_redis_value

        redis_cache_data_null = await redis_handler.get(key="wrong_key_test")
        assert redis_cache_data_null == None