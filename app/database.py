from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
# from .config import settings

SQLALCHEMY_DATABASE_URL = "postgresql://therapistdb_owner:DKqcQ95rpZHg@ep-winter-dawn-a5sqe29h.us-east-2.aws.neon.tech/therapistdb?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()