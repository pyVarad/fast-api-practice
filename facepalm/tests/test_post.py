import pytest
from httpx import AsyncClient


async def create_post(body:str, async_client:AsyncClient) -> dict:
    response = async_client.post("/posts", json={"body": body})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test_Post", async_client)