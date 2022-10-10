# pylint: disable=unused-argument

import pytest
from fastapi import status

from bookmarker.config import get_settings
from bookmarker.utils import user


pytestmark = pytest.mark.asyncio


class BaseHandler:
    settings = get_settings()

    @classmethod
    def get_url(cls, path: str) -> str:
        return f"{cls.settings.PATH_PREFIX}/user/{path}"


class TestAuthenticationHandler(BaseHandler):
    @staticmethod
    def get_data(username: str, password: str) -> dict:
        return {"username": username, "password": password}

    async def test_authentication_no_data(self, client):
        response = await client.post(url=self.get_url("authentication"))
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()

    async def test_authentication_no_user(self, client, test_user_data):
        response = await client.post(
            url=self.get_url("authentication"), data=self.get_data(test_user_data.username, test_user_data.password)
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    async def test_authentication_wrong_password(self, client, created_user):
        response = await client.post(
            url=self.get_url("authentication"), data=self.get_data(created_user.data.username, "wrong_password")
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    async def test_authentication_success(self, client, created_user):
        response = await client.post(
            url=self.get_url("authentication"),
            data=self.get_data(created_user.data.username, created_user.data.password),
        )
        assert response.status_code == status.HTTP_200_OK, response.json()


class TestRegistrationHandler(BaseHandler):
    @classmethod
    def get_data(cls, username: str, password: str, email: str | None = None) -> dict:
        return {"username": username, "password": cls.settings.PWD_CONTEXT.hash(password), "email": email}

    async def test_registration_no_data(self, client):
        response = await client.post(url=self.get_url("registration"))
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()

    async def test_registration_exists(self, client, created_user, potential_user):
        response = await client.post(url=self.get_url("registration"), content=potential_user.json())
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()

    async def test_registration_empty(self, client, created_user):
        response = await client.post(url=self.get_url("registration"), data=self.get_data(username="", password=""))
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()

    async def test_registration_empty_password(self, client, created_user):
        response = await client.post(
            url=self.get_url("registration"), data=self.get_data(username="username", password="")
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()

    async def test_registration_empty_username(self, client, created_user):
        response = await client.post(
            url=self.get_url("registration"), data=self.get_data(username="", password="password")
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()

    async def test_registration_less_than_min_value_password(self, client, created_user):
        response = await client.post(
            url=self.get_url("registration"), data=self.get_data(username="username", password="p")
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()

    async def test_registration_less_than_min_value_username(self, client, created_user):
        response = await client.post(
            url=self.get_url("registration"), data=self.get_data(username="u", password="password")
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.json()

    async def test_registration_ok(self, database, client, potential_user):
        assert await user.get_user(database, potential_user.username) is None
        response = await client.post(url=self.get_url("registration"), content=potential_user.json())
        assert response.status_code == status.HTTP_201_CREATED, response.json()
        assert await user.get_user(database, potential_user.username) is not None


class TestGetMeHandler(BaseHandler):
    async def test_get_me_no_token(self, client):
        response = await client.get(url=self.get_url("me"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    async def test_get_me_bad_token(self, client):
        response = await client.get(url=self.get_url("me"), headers={"Authorization": "Bearer wrong_token"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    async def test_get_me_bad_token_no_username(self, client):
        response = await client.get(
            url=self.get_url("me"), headers={"Authorization": f"Bearer {user.create_access_token(data={})}"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    async def test_get_me_bad_token_no_user(self, client, test_user_data):
        response = await client.get(
            url=self.get_url("me"),
            headers={"Authorization": f"Bearer {user.create_access_token(data={'sub': test_user_data.username})}"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    async def test_get_me_ok(self, client, created_user, user_headers):
        response = await client.get(url=self.get_url("me"), headers=user_headers)
        assert response.status_code == status.HTTP_200_OK, response.json()
        assert response.json()["username"] == created_user.data.username


class TestTakeoutHandle(BaseHandler):
    async def test_delete_no_user(self, database, client, user_headers):
        response = await client.delete(url=self.get_url("takeout"), headers=user_headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()

    async def test_delete_ok(self, database, client, created_user, user_headers):
        assert await user.get_user(database, created_user.data.username) is not None
        response = await client.delete(url=self.get_url("takeout"), headers=user_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()
        assert await user.get_user(database, created_user.data.username) is None
