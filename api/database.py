import os
from contextlib import contextmanager
from sqlmodel import create_engine, Session

# Load from environment or fall back to default (used in local Docker Compose)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@database:5432/alpha"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=False)


# Database session generator
def get_db_session():
    with Session(engine) as session:
        yield session


db_context = contextmanager(get_db_session)