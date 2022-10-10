# pylint: disable=unused-argument
# pylint: disable=too-many-arguments
import uuid

import pytest
from sqlalchemy import select

from bookmarker.db.enums import BookmarksSortKey
from bookmarker.db.models import Bookmark, Tag
from bookmarker.utils import bookmark


pytestmark = pytest.mark.asyncio


class TestCreateBookmarkHandler:
    @staticmethod
    async def assert_bookmark_created(database, data, bookmark_data):
        assert data.title == bookmark_data.title
        assert data.link == bookmark_data.link
        assert data.tag == bookmark_data.tag

        search_bookmark_query = select(Bookmark).where(Bookmark.id == data.id)
        bookmark_model = await database.scalar(search_bookmark_query)
        assert bookmark_model is not None

    async def test_create_bookmark_no_tag(
        self, database, created_user, test_bookmark_no_tag_data, bookmark_no_tag_schema
    ):
        data = await bookmark.create_bookmark(
            database, created_user.model, bookmark_no_tag_schema, test_bookmark_no_tag_data.title
        )
        await self.assert_bookmark_created(database, data, test_bookmark_no_tag_data)

    async def test_create_bookmark_new_tag(self, database, created_user, test_bookmark_data, bookmark_schema):
        data = await bookmark.create_bookmark(database, created_user.model, bookmark_schema, test_bookmark_data.title)
        await self.assert_bookmark_created(database, data, test_bookmark_data)

        search_tag_query = select(Tag).where(Tag.name == bookmark_schema.tag)
        tag = await database.scalar(search_tag_query)
        assert tag is not None
        assert tag.name == data.tag

    async def test_create_bookmark_existing_tag(
        self, database, created_user, test_bookmark_data, bookmark_schema, created_tag
    ):
        data = await bookmark.create_bookmark(database, created_user.model, bookmark_schema, test_bookmark_data.title)
        await self.assert_bookmark_created(database, data, test_bookmark_data)


class TestGetBookmarkHandler:
    async def test_get_bookmark_no_bookmark(self, database, created_user, test_bookmark_data):
        assert await bookmark.get_bookmark(database, created_user.model, uuid.uuid4()) is None

    async def test_get_bookmark_ok(self, database, created_user, created_bookmark):
        bookmark_schema = await bookmark.get_bookmark(database, created_user.model, created_bookmark.model.id)
        assert bookmark_schema is not None
        assert bookmark_schema.id == created_bookmark.model.id


class TestDeleteBookmarkHandler:
    async def test_delete_bookmark_no_bookmark(self, database, created_user):
        await bookmark.delete_bookmark(session=database, owner=created_user.model, bookmark_id=uuid.uuid4())

    async def test_delete_bookmark_ok(self, database, created_user, created_bookmark):
        await bookmark.delete_bookmark(
            session=database, owner=created_user.model, bookmark_id=created_bookmark.model.id
        )
        bookmark_model = await bookmark.get_bookmark(
            session=database, owner=created_user.model, bookmark_id=created_bookmark.model.id
        )  # REVIEW: best practice?
        assert bookmark_model is None


class TestBuildQueryForRetrieveListOfBookmarksHandler:  # REVIEW: best practice for assert select?
    @staticmethod
    def compare_select(select_query, expected_query):
        return select_query.compile().string == expected_query.compile().string

    async def test_build_query_for_retrieve_list_of_bookmarks_no_tag_ok(self, created_user):
        assert self.compare_select(
            bookmark.build_query_for_retrieve_list_of_bookmarks(created_user.model, [], None),
            select(Bookmark).filter(Bookmark.owner_id == created_user.model.id).order_by(Bookmark.id),
        )

    async def test_build_query_for_retrieve_list_of_bookmarks_one_tag_sort_date_ok(self, created_user):
        tag_filter = ["tag"]
        assert self.compare_select(
            bookmark.build_query_for_retrieve_list_of_bookmarks(
                created_user.model, tag_filter, BookmarksSortKey.BY_DATE
            ),
            select(Bookmark)
            .filter(Bookmark.owner_id == created_user.model.id)
            .filter(Bookmark.tag.in_(tag_filter))
            .order_by(Bookmark.dt_created),
        )

    async def test_build_query_for_retrieve_list_of_bookmarks_many_tag_sort_link_ok(self, created_user):
        tag_filter = ["tag1", "tag2", "tag3"]
        assert self.compare_select(
            bookmark.build_query_for_retrieve_list_of_bookmarks(
                created_user.model, tag_filter, BookmarksSortKey.BY_LINK
            ),
            select(Bookmark)
            .filter(Bookmark.owner_id == created_user.model.id)
            .filter(Bookmark.tag.in_(tag_filter))
            .order_by(Bookmark.link),
        )

    async def test_build_query_for_retrieve_list_of_bookmarks_many_tag_no_sort_ok(self, created_user):
        tag_filter = ["tag1", "tag2", "tag3"]
        assert self.compare_select(
            bookmark.build_query_for_retrieve_list_of_bookmarks(created_user.model, tag_filter, None),
            select(Bookmark)
            .filter(Bookmark.owner_id == created_user.model.id)
            .filter(Bookmark.tag.in_(tag_filter))
            .order_by(Bookmark.id),
        )

    async def test_build_query_for_retrieve_list_of_bookmarks_many_tag_sort_id_ok(self, created_user):
        tag_filter = ["tag1", "tag2", "tag3", "tag4", "tag5"]
        assert self.compare_select(
            bookmark.build_query_for_retrieve_list_of_bookmarks(created_user.model, tag_filter, BookmarksSortKey.BY_ID),
            select(Bookmark)
            .filter(Bookmark.owner_id == created_user.model.id)
            .filter(Bookmark.tag.in_(tag_filter))
            .order_by(Bookmark.id),
        )

    async def test_build_query_for_retrieve_list_of_bookmarks_no_tag_sort_title_ok(self, created_user):
        assert self.compare_select(
            bookmark.build_query_for_retrieve_list_of_bookmarks(created_user.model, [], BookmarksSortKey.BY_TITLE),
            select(Bookmark).filter(Bookmark.owner_id == created_user.model.id).order_by(Bookmark.title),
        )
