import uvicorn

from app.creator import create_app
from config import settings

if __name__ == '__main__':
    app = create_app()
    uvicorn.run(
        app,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level='debug' if settings.APP_DEBUG else 'info',
    )
