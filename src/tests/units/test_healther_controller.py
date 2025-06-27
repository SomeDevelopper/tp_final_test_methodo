import pytest
from src.controllers.healther_controller import health_check

@pytest.mark.asyncio
async def test_health_check():
    response = await health_check()
    assert response.get('status') == 'ok'