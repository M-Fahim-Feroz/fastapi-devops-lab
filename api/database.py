import os
from contextlib import contextmanager
from sqlmodel import create_engine, Session

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://user:password@database:5432/alpha"
)

engine = create_engine(DATABASE_URL)


def get_db_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


db_context = contextmanager(get_db_session)
