# pylint: disable=unused-argument

import pytest

from bookmarker.utils import bookmark


pytestmark = pytest.mark.asyncio


class TestGetPageTitleHandler:
    async def test_get_page_title(self, client):
        assert bookmark.get_page_title("https://www.example.com") is not None
