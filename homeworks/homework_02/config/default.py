import logging
from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent

logging_format = (
    '%(filename)s %(funcName)s [LINE:%(lineno)d]# '
    '%(levelname)-8s [%(asctime)s] %(name)s: %(message)s'
)

logging.basicConfig(
    format=logging_format,
    level=logging.INFO,
    filename='app.log',
)


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    ENV: str = Field('local', env='ENV')
    PATH_PREFIX: str = Field('', end='PATH_PREFIX')
    APP_HOST: str = Field('0.0.0.0', env='APP_HOST')
    APP_PORT: int = Field(8090, env='APP_PORT')
    APP_DEBUG: bool = Field(True, env='DEBUG')

    DB_NAME: str = Field('pharmacy', env='DB_NAME')
    DB_PATH: str = Field('localhost', env='DB_PATH')
    DB_USER: str = Field('student', env='DB_USER')
    DB_PORT: int = Field(5432, env='DB_PORT')
    DB_PASSWORD: str = Field('shbr2022', env='DB_PASSWORD')
    DB_POOL_SIZE: int = Field(15, env='DB_POOL_SIZE')
    DB_CONNECT_RETRY: int = Field(20, env='DB_CONNECT_RETRY')

    @property
    def database_settings(self) -> dict[str, int | str]:
        """
        Get all settings for connection with database.
        """
        return {
            'database': self.DB_NAME,
            'user': self.DB_USER,
            'password': self.DB_PASSWORD,
            'host': self.DB_PATH,
            'port': self.DB_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return (
            'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
                **self.database_settings,
            )
        )

    class Config:
        env_file: Path = BASE_DIR / '.env'
