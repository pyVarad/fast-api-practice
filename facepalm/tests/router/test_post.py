import pytest
from httpx import AsyncClient


async def create_post(body:str, async_client:AsyncClient) -> dict:
    response = await async_client.post("/posts/", json={"body": body})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test_Post", async_client)


@pytest.mark.anyio
async def test_simple_post(async_client: AsyncClient):
    body = "Test body"
    response = await async_client.post("/posts/", json={"body": body})
    assert response.status_code == 201
    assert {"id": 1, "body": body}.items() <= response.json().items()

@pytest.mark.anyio
async def test_post_without_body(async_client: AsyncClient):
    response = await async_client.post("/posts/", json={})
    assert response.status_code == 422

@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/posts/")
    assert response.status_code == 200
    assert response.json() == [created_post]