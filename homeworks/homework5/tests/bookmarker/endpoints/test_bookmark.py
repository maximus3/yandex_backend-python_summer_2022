# pylint: disable=too-many-arguments
# pylint: disable=unused-argument

import uuid

import pytest
from fastapi import status
from sqlalchemy import select

from bookmarker.config import get_settings
from bookmarker.db.enums import BookmarksSortKey
from bookmarker.db.models import Bookmark


pytestmark = pytest.mark.asyncio


class BaseHandler:
    settings = get_settings()

    @classmethod
    def get_url(cls, path: str) -> str:
        return f"{cls.settings.PATH_PREFIX}/bookmark{'/' if path else ''}{path}"


class TestCreateHandler(BaseHandler):
    @staticmethod
    async def assert_model_created(database, response):
        search_bookmark_query = select(Bookmark).where(Bookmark.id == response.json().get("id"))
        bookmark_model = await database.scalar(search_bookmark_query)
        assert bookmark_model is not None

    async def test_create_no_auth(self, client):
        response = await client.post(url=self.get_url(""))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    async def test_create_no_data(self, client, created_user, user_headers):
        response = await client.post(url=self.get_url(""), headers=user_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()

    async def test_create_no_tag_ok(self, database, client, created_user, bookmark_no_tag_schema, user_headers):
        response = await client.post(url=self.get_url(""), content=bookmark_no_tag_schema.json(), headers=user_headers)
        assert response.status_code == status.HTTP_201_CREATED, response.json()
        await self.assert_model_created(database, response)

    async def test_create_ok(self, database, client, created_user, bookmark_schema, user_headers):
        response = await client.post(url=self.get_url(""), content=bookmark_schema.json(), headers=user_headers)
        assert response.status_code == status.HTTP_201_CREATED, response.json()
        await self.assert_model_created(database, response)


class TestRetrieveHandler(BaseHandler):
    async def test_retrieve_no_auth(self, client, created_bookmark):
        response = await client.get(url=self.get_url(created_bookmark.model.id))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    async def test_retrieve_bad_id(self, client, created_user, user_headers):
        response = await client.get(url=self.get_url("bad_id"), headers=user_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()

    async def test_retrieve_no_bookmark(self, client, created_user, user_headers):
        response = await client.get(url=self.get_url(str(uuid.uuid4())), headers=user_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()

    async def test_retrieve_ok(self, client, created_bookmark, created_user, user_headers):
        response = await client.get(url=self.get_url(created_bookmark.model.id), headers=user_headers)
        assert response.status_code == status.HTTP_200_OK, response.json()
        assert response.json().get("id") == str(created_bookmark.model.id)


class TestDeleteHandler(BaseHandler):
    async def test_delete_no_auth(self, client, created_bookmark):
        response = await client.delete(url=self.get_url(created_bookmark.model.id))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    async def test_delete_bad_id(self, client, created_user, user_headers):
        response = await client.delete(url=self.get_url("bad_id"), headers=user_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()

    async def test_delete_404(self, client, created_user, user_headers):
        response = await client.delete(url=self.get_url(str(uuid.uuid4())), headers=user_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()

    async def test_delete_ok(self, database, client, created_bookmark, created_user, user_headers):
        response = await client.delete(url=self.get_url(created_bookmark.model.id), headers=user_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
        assert await database.scalar(select(Bookmark).where(Bookmark.id == created_bookmark.model.id)) is None


class TestRetrieveListHandler(BaseHandler):
    @staticmethod
    def get_data(tag_filter: list[str], sort_key: BookmarksSortKey | None = None) -> dict:
        res = {"tag": tag_filter}
        if sort_key:
            res.update({"sort_key": sort_key.value})
        return res

    async def test_retrieve_list_no_auth(self, client, created_bookmark):
        response = await client.get(url=self.get_url(""), params=self.get_data([]))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    async def test_retrieve_list_ok_empty(self, client, created_user, user_headers):
        response = await client.get(url=self.get_url(""), headers=user_headers, params=self.get_data([]))
        assert response.status_code == status.HTTP_200_OK, response.json()
        assert response.json().get("total") == 0, response.json()

    async def test_retrieve_list_ok(self, client, created_bookmark, created_user, user_headers):
        response = await client.get(url=self.get_url(""), headers=user_headers, params=self.get_data([]))
        assert response.status_code == status.HTTP_200_OK, response.json()
        assert response.json().get("total") == 1, response.json()
