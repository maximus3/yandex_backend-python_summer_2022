from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette import status

from shortener.db.connection import get_db
from shortener.db.models import UrlStorage
from shortener.utils import check_vip_expired


api_router = APIRouter(tags=["Url"])


@api_router.get(
    "/{short_code}",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    responses={status.HTTP_404_NOT_FOUND: {"description": "URL `request.url` doesn't exist"}},
)
async def get_long_url(
    request: Request,
    short_code: str = Path(...),
    db: Session = Depends(get_db),
):
    """
    Логика работы ручки:

    Проверяем, что у нас есть short_code в базе:
      - если он уже есть, то совершаем редирект на длинный урл + увеличиваем счетчик переходов на 1
      - если нет, то кидаем ошибку;
    """
    db_url = db.query(UrlStorage).where(UrlStorage.short_url == short_code).first()
    if db_url and (not db_url.is_vip or not check_vip_expired(db_url, db)):
        db_url.number_of_clicks += 1
        db.commit()
        return RedirectResponse(db_url.long_url)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"URL '{request.url}' doesn't exist")
