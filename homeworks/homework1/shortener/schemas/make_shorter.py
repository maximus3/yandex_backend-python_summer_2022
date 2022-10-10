from enum import Enum, unique

from pydantic import UUID4, AnyUrl, BaseModel, Field


@unique
class TimeToLiveUnit(str, Enum):
    SECONDS = "SECONDS"
    MINUTES = "MINUTES"
    HOURS = "HOURS"
    DAYS = "DAYS"


class MakeShorterRequest(BaseModel):
    url: AnyUrl = Field(title="URL to be shortened")
    vip_key: str | None = Field(title="VIP key", description="Short key to be mapped to long url")
    time_to_live: int = Field(
        title="Time to live",
        default=10,
        description="Number of time-units this short url is going to be active. "
        "Maximum value must not be more than 48 hours",
    )
    time_to_live_unit: TimeToLiveUnit = Field(
        title="Time to live unit", default=TimeToLiveUnit.HOURS, description="Time unit for time_to_live parameter"
    )


class MakeShorterResponse(BaseModel):
    short_url: AnyUrl = Field(title="Shortened URL")
    secret_key: UUID4

    class Config:
        orm_mode = True
