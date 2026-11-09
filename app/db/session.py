from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()