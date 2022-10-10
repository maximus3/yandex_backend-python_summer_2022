# pylint: disable=unused-argument

import pytest

from bookmarker.utils import user


pytestmark = pytest.mark.asyncio


class TestGetUserHandler:
    async def test_get_user_no_user(self, database, test_user_data):
        assert (
            await user.get_user(session=database, username=test_user_data.username) is None
        )  # REVIEW: check get from db manually?

    async def test_get_user_ok(self, database, created_user):
        user_model = await user.get_user(session=database, username=created_user.data.username)
        assert user_model
        assert user_model == created_user.model


class TestRegisterUserHandler:
    async def test_register_user_exists(self, database, potential_user, created_user):
        is_ok, _ = await user.register_user(session=database, potential_user=potential_user)
        assert not is_ok

    async def test_register_user_ok(self, database, potential_user):
        is_ok, _ = await user.register_user(session=database, potential_user=potential_user)
        assert is_ok


class TestDeleteUserHandler:
    async def test_delete_user_ok(self, database, created_user):
        await user.delete_user(session=database, user=created_user.model)
        user_model = await user.get_user(
            session=database, username=created_user.data.username
        )  # REVIEW: best practice?
        assert user_model is None
