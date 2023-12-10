from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from src.settings import PostgresSettings

settings = PostgresSettings()
DATABASE_URL = (
    f"postgresql://"
    f"{settings.postgres_user}:"
    f"{settings.postgres_password}@"
    f"{settings.postgres_uri}:"
    f"{settings.postgres_port}/"
    f"{settings.postgres_db}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Session:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
