from contextlib import contextmanager
from typing import Any

import sqlalchemy as sa
from sqlalchemy.orm import Session as SessionType
from sqlalchemy.orm import scoped_session, sessionmaker

from config import settings

engine = sa.create_engine(settings.database_uri)
Session = scoped_session(sessionmaker(bind=engine))


@contextmanager
def create_session(**kwargs: Any) -> SessionType:
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()
