import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

os.environ["ENV_STATE"] = "test"
from facepalm.database import database
from facepalm.main import app  #noqa: E402


# 1. Add the anyio_backed as method for any pytest api.
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

# 2. Create client fixture using TestClient package utils from fastapi.
@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)

# 3. Clear the db before executing each test. Hence set the `autouse` to True.
@pytest.fixture(autouse=True)
async def db():
    await database.connect()
    yield
    await database.disconnect()

# 4. Generate async_client fixture which uses the client fixture to generate async client.
@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=client.base_url) as ac:
        yield ac