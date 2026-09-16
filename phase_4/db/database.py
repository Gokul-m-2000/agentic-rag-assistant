from sqlalchemy import create_engine
from settings import settings
from sqlalchemy.orm import sessionmaker

engine=create_engine(
    settings.database_url)


SessionLocal=sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)