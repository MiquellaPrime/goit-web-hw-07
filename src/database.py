from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings

if settings.IS_DEV:
    engine = create_engine(
        url="sqlite:///university.db",
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(url=settings.db.postgres_dsn)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
