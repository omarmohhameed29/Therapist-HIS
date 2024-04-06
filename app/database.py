from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from .config import settings

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


#          testing connection
# from sqlalchemy import create_engine, text
# from sqlalchemy.exc import SQLAlchemyError

# # Define your connection string for the Neon PostgreSQL database
# NEON_POSTGRES_CONNECTION_STRING = "postgresql://therapistdb_owner:DKqcQ95rpZHg@ep-winter-dawn-a5sqe29h.us-east-2.aws.neon.tech/therapistdb?sslmode=require"

# try:
#     # Create the SQLAlchemy engine using the connection string
#     engine = create_engine(NEON_POSTGRES_CONNECTION_STRING)
    
#     # Attempt to connect to the database
#     with engine.connect() as connection:
#         print("Connection to the database is successful.")
        
#         # Define the SQL statement as a SQLAlchemy text construct
#         sql_statement = text("SELECT * FROM playing_with_neon")
        
#         # Execute the query
#         result = connection.execute(sql_statement)
        
#         # Fetch the result
#         row = result.fetchone()
#         if row:
#             print("Query executed successfully. Result:", row)
#         else:
#             print("No results found for the query.")
        
# except SQLAlchemyError as e:
#     print("Error connecting to the database:", e)