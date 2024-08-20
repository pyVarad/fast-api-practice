import pytest
from httpx import AsyncClient


async def create_post(body:str, async_client:AsyncClient) -> dict:
    response = await async_client.post("/posts/", json={"body": body})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test_Post", async_client)

@pytest.fixture()
async def add_new_comment(async_client:AsyncClient, created_post: dict):
    response = await async_client.post("/posts/1/comment", json={"body": "Sample comment"})
    return response.json()


@pytest.mark.anyio
async def test_get_all_comments(async_client:AsyncClient, add_new_comment: dict):
    response = await async_client.get("/posts/1")
    assert response.status_code == 200
