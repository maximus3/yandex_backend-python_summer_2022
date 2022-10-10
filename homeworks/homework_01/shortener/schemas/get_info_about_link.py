from datetime import datetime

from pydantic import AnyUrl, BaseModel


class GetInfoAboutLinkResponse(BaseModel):
    short_url: AnyUrl
    long_url: AnyUrl
    number_of_clicks: int
    dt_created: datetime
    is_vip: bool
    dt_expiration: datetime | None

    class Config:
        orm_mode = True
