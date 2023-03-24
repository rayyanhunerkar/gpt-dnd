import pytest


@pytest.mark.asyncio
async def test_health(test_client):
    response = await test_client.get("/api/ping")
    assert response.status_code == 200
