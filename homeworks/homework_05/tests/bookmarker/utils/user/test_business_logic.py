from datetime import timedelta

import pytest
from fastapi import HTTPException

from bookmarker.config import get_settings
from bookmarker.utils import user


pytestmark = pytest.mark.asyncio


class TestAuthenticateUserHandler:
    async def test_authenticate_user_no_username(self, database, test_user_data):
        assert not await user.authenticate_user(database, test_user_data.username, test_user_data.password)

    async def test_authenticate_user_wrong_password(self, database, created_user):
        assert not await user.authenticate_user(database, created_user.data.username, "wrong_password")

    async def test_authenticate_user_ok(self, database, created_user):
        assert await user.authenticate_user(database, created_user.data.username, created_user.data.password)


class TestCreateAccessTokenHandler:  # REVIEW: best practice for const strings?
    async def test_create_access_token_with_expires_delta(self):
        access_token_expires = timedelta(minutes=1)
        assert (
            user.create_access_token(data={"sub": "test"}, expires_delta=access_token_expires) is not None
        )  # REVIEW: how check valid token?

    async def test_create_access_token(self):
        assert user.create_access_token(data={"sub": "test"}) is not None  # REVIEW: how check valid token?


class TestVerifyPasswordHandler:
    async def test_verify_password_ok(self, test_user_data, potential_user):
        assert user.verify_password(test_user_data.password, potential_user.password)

    async def test_verify_password_wrong_password(self):
        settings = get_settings()
        hashed_wrong_password = settings.PWD_CONTEXT.hash("wrong_password")
        assert not user.verify_password("password", hashed_wrong_password)


class TestGetCurrentUserHandler:
    async def test_get_current_user_no_token(self, database):
        with pytest.raises(HTTPException):
            await user.get_current_user(database, "")

    async def test_get_current_user_username_none(self, database):
        with pytest.raises(HTTPException):
            await user.get_current_user(database, user.create_access_token(data={}))

    async def test_get_current_user_user_none(self, database, test_user_data):
        with pytest.raises(HTTPException):
            await user.get_current_user(database, user.create_access_token(data={"sub": test_user_data.username}))

    async def test_get_current_user_ok(self, database, created_user):
        user_model = await user.get_current_user(
            database, user.create_access_token(data={"sub": created_user.data.username})
        )
        assert user_model is not None
        assert user_model == created_user.model
