from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL")

postgres_engine = create_engine(SQLALCHEMY_DATABASE_URL)
PostgresSession = sessionmaker(autocommit=False, autoflush=False, bind=postgres_engine)

