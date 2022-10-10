from logging import getLogger

from fastapi import FastAPI

from app.endpoints import list_of_routes
from config import DefaultSettings, settings

logger = getLogger(__name__)


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


# def init_database() -> None:
#     """
#     Creates a reusable database connection.
#     Check before launching the application that the database is available to it.
#     """
#     SessionManager()


def create_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = 'Микросервис, проверяющий состав корзины в онлайн аптеке.'

    tags_metadata = [
        {
            'name': 'Url',
            'description': 'Pharmacy shopping cart checker.',
        },
        {
            'name': 'Health check',
            'description': 'API health check.',
        },
    ]

    application = FastAPI(
        title='Pharmacy shopping cart checker',
        description=description,
        docs_url='/swagger',
        openapi_url='/openapi',
        version='1.0.0',
        openapi_tags=tags_metadata,
    )
    bind_routes(application, settings)
    application.state.settings = settings
    # init_database()
    return application
