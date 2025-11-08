import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_and_get_item(async_client: AsyncClient = None):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create item
        payload = {"title": "integration_item", "description": "test"}
        res = await client.post("/api/v1/testroute/items", json=payload)
        assert res.status_code == 201
        data = res.json()
        assert data["title"] == "integration_item"

        # Fetch by ID
        item_id = data["id"]
        res2 = await client.get(f"/api/v1/testroute/items/{item_id}")
        assert res2.status_code == 200
        assert res2.json()["title"] == "integration_item"
