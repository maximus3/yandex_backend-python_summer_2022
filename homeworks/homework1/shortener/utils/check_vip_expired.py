from datetime import datetime, timezone

from sqlalchemy.orm import Session

from shortener.db.models import UrlStorage


def check_vip_expired(db_url: UrlStorage, db: Session) -> bool:
    """
    Check if VIP key is expired and delete if it is
    """
    if db_url.dt_expiration > datetime.now(tz=timezone.utc):
        return False
    db.delete(db_url)
    db.commit()
    return True
