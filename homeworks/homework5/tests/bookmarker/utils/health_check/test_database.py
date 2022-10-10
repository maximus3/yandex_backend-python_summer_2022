import pytest

from bookmarker.utils import health_check


pytestmark = pytest.mark.asyncio


class TestHealthCheckDbHandler:
    async def test_health_check_db(self, database):
        assert await health_check.health_check_db(database)
