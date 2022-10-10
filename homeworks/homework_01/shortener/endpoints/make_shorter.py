from datetime import datetime, timedelta, timezone
from random import choice
from string import ascii_uppercase, digits

from fastapi import APIRouter, Body, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import exists
from sqlalchemy.orm import Session
from starlette import status

from shortener import utils
from shortener.db.connection import get_db
from shortener.db.models import UrlStorage
from shortener.schemas import MakeShorterRequest, MakeShorterResponse
from shortener.schemas.make_shorter import TimeToLiveUnit


api_router = APIRouter(tags=["Url"])


def get_short(db: Session, suffix: str = None) -> tuple[str, str]:
    while suffix is None:
        suffix = "".join(choice(ascii_uppercase + digits) for _ in range(5))
        exist = db.query(exists().where(UrlStorage.short_url == suffix)).scalar()
        if not exist:
            break
        suffix = None
    short_url = utils.url_from_suffix(suffix)
    return short_url, suffix


@api_router.post(
    "/make_shorter",
    response_model=MakeShorterResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Site with this url does not exists or status code of request >= 400",
        },
    },
)
async def make_shorter(
    model: MakeShorterRequest = Body(..., example={"url": "https://yandex.ru"}),
    db: Session = Depends(get_db),
):
    """
    Логика работы ручки:

    Проверяем, что у нас еще нет сокращенного варианта урла для переданного длинного адреса
      - если он уже есть, то возвращаем его
      - если еще нет:
          1) Подбираем маленький суффикс, которого еще нет в базе;
          2) Сохраняем этот суффикс в базу;
          3) На основе этого суффикса и текущих настроек приложения генерируем полноценный урл;
          4) Возвращаем результат работы ручки: урл и secret_key для запроса дополнительной информации.
    """
    is_vip = model.vip_key is not None

    dt_expiration = None
    if is_vip:
        # Check if short url is already exists
        db_url = db.query(UrlStorage).where(UrlStorage.short_url == str(model.vip_key)).first()
        exist = db_url is not None
        if exist and not utils.check_vip_expired(db_url, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="VIP key is already exists",
            )
        timedelta_to_expiration = timedelta(
            days=model.time_to_live if model.time_to_live_unit == TimeToLiveUnit.DAYS else 0,
            hours=model.time_to_live if model.time_to_live_unit == TimeToLiveUnit.HOURS else 0,
            minutes=model.time_to_live if model.time_to_live_unit == TimeToLiveUnit.MINUTES else 0,
            seconds=model.time_to_live if model.time_to_live_unit == TimeToLiveUnit.SECONDS else 0,
        )
        if timedelta_to_expiration > timedelta(days=2):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="VIP key expiration time is too big",
            )
        dt_expiration = datetime.now(tz=timezone.utc) + timedelta_to_expiration
    else:
        # Check if long url is already exists
        db_url = db.query(UrlStorage).where(UrlStorage.long_url == str(model.url)).first()
        exist = db_url is not None
        if exist:
            db_url.short_url = utils.url_from_suffix(db_url.short_url)
            return MakeShorterResponse.from_orm(db_url)

    valid_site, message = await utils.check_website_exist(model.url)
    if not valid_site:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
    _, suffix = get_short(db, suffix=model.vip_key)
    new_url = UrlStorage(long_url=str(model.url), short_url=suffix, is_vip=is_vip, dt_expiration=dt_expiration)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    new_url.short_url = utils.url_from_suffix(suffix)
    return MakeShorterResponse.from_orm(new_url)
