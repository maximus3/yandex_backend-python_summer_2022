# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument

from asyncio import new_event_loop, set_event_loop
from contextlib import AsyncExitStack, asynccontextmanager
from os import environ
from types import SimpleNamespace
from uuid import uuid4

import pytest
from alembic.command import upgrade
from alembic.config import Config
from httpx import AsyncClient
from mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import create_database, database_exists, drop_database

from tests.utils import BookmarkData, DataAndModel, TagData, UserData, make_alembic_config

from bookmarker.__main__ import get_app
from bookmarker.config import get_settings
from bookmarker.db.connection import SessionManager, get_session
from bookmarker.db.models import Bookmark, Tag, User
from bookmarker.schemas import BookmarkCreateRequest, RegistrationForm
from bookmarker.utils import bookmark as utils_module
from bookmarker.utils import user


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    loop = new_event_loop()
    set_event_loop(loop)

    yield loop
    loop.close()


@pytest.fixture()
def postgres() -> str:
    """
    Создает временную БД для запуска теста.
    """
    settings = get_settings()

    tmp_name = ".".join([uuid4().hex, "pytest"])
    settings.POSTGRES_DB = tmp_name
    environ["POSTGRES_DB"] = tmp_name

    tmp_url = settings.database_uri_sync
    if not database_exists(tmp_url):
        create_database(tmp_url)

    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture()
def postgres_engine(postgres):
    """
    SQLAlchemy engine, bound to temporary database.
    """
    engine = create_engine(postgres)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def alembic_config(postgres) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(config="bookmarker/db/", name="alembic", pg_url=postgres, raiseerr=False, x=None)
    return make_alembic_config(cmd_options)


@pytest.fixture
def migrated_postgres(alembic_config: Config):
    """
    Проводит миграции.
    """
    upgrade(alembic_config, "head")


@pytest.fixture
async def client(migrated_postgres, manager: SessionManager = SessionManager()) -> AsyncClient:
    """
    Returns a client that can be used to interact with the application.
    """
    app = get_app()
    manager.refresh()  # без вызова метода изменения конфига внутри фикстуры postgres не подтягиваются в класс
    utils_module.get_page_title = Mock(return_value="Title")
    yield AsyncClient(app=app, base_url="http://test")


@pytest.fixture
async def database(postgres, migrated_postgres, manager: SessionManager = SessionManager()) -> AsyncSession:
    """
    Returns a class object with which you can create a new session to connect to the database.
    """
    manager.refresh()  # без вызова метода изменения конфига внутри фикстуры postgres не подтягиваются в класс
    context_manager = asynccontextmanager(get_session)()
    database = await AsyncExitStack().enter_async_context(context_manager)
    try:
        yield database
    finally:
        await database.close()


@pytest.fixture
def test_user_data():
    return UserData(username="username", password="password", email="email@example.com")


@pytest.fixture
def potential_user(test_user_data):
    return RegistrationForm(
        username=test_user_data.username, password=test_user_data.password, email=test_user_data.email
    )


@pytest.fixture
async def created_user(database, potential_user, test_user_data):
    user = User(**potential_user.dict(exclude_unset=True))
    database.add(user)
    await database.commit()
    await database.refresh(user)
    return DataAndModel(data=test_user_data, model=user)


@pytest.fixture
def user_token(test_user_data):
    return user.create_access_token(data={"sub": test_user_data.username})


@pytest.fixture
def user_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def test_bookmark_no_tag_data():
    return BookmarkData(link="http://example.com/", tag=None, title="title")


@pytest.fixture
def bookmark_no_tag_schema(test_bookmark_no_tag_data):
    return BookmarkCreateRequest(link=test_bookmark_no_tag_data.link, tag=test_bookmark_no_tag_data.tag)


@pytest.fixture
def test_tag_data():
    return TagData(name="tag")


@pytest.fixture
async def created_tag(database, test_tag_data):
    tag = Tag(name=test_tag_data.name)
    database.add(tag)
    await database.commit()
    await database.refresh(tag)
    return DataAndModel(data=test_tag_data, model=tag)


@pytest.fixture
def test_bookmark_data(test_tag_data, test_bookmark_no_tag_data):
    return BookmarkData(
        link=test_bookmark_no_tag_data.link, tag=test_tag_data.name, title=test_bookmark_no_tag_data.title
    )


@pytest.fixture
def bookmark_schema(test_bookmark_data):
    return BookmarkCreateRequest(link=test_bookmark_data.link, tag=test_bookmark_data.tag)


@pytest.fixture
async def created_bookmark(database, test_bookmark_data, created_tag, created_user):
    bookmark = Bookmark(
        title=test_bookmark_data.title,
        link=test_bookmark_data.link,
        tag=created_tag.model.name,
        owner_id=created_user.model.id,
    )
    database.add(bookmark)
    await database.commit()
    await database.refresh(bookmark)
    return DataAndModel(data=test_bookmark_data, model=bookmark)
