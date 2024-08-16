import pytest
from fastapi.testclient import TestClient

from httpx import AsyncClient
from facepalm.main import app
from facepalm.router.post import all_comments, all_posts

from typing import Generator, AsyncGenerator


@pytest.fixture(scope="session")
async def anyio_bckend():
    return "asyncio"

@pytest.fixture
def client() -> Generator:
    yield TestClient(app)

@pytest.fixture(autouse=True)
async def db():
    all_comments.clear()
    all_posts.clear()
    yield

@pytest.fixture
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac