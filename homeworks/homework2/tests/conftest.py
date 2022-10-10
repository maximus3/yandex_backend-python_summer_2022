import pytest
from httpx import AsyncClient

from app.creator import create_app


@pytest.fixture()
async def client():
    async with AsyncClient(
        app=create_app(), base_url='http://localhost:8090/'
    ) as client:
        yield client
