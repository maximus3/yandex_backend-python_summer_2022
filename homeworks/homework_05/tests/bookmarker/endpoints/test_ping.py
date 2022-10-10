import pytest
from fastapi import status


pytestmark = pytest.mark.asyncio


class TestHealthCheckHandler:
    @staticmethod
    def get_url_application() -> str:
        return "/api/v1/health_check/ping_application"

    @staticmethod
    def get_url_database() -> str:
        return "/api/v1/health_check/ping_database"

    async def test_ping_application(self, client):
        response = await client.get(url=self.get_url_application())
        assert response.status_code == status.HTTP_200_OK

    async def test_ping_database(self, client):
        response = await client.get(url=self.get_url_database())
        assert response.status_code == status.HTTP_200_OK
