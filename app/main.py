from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello World"}





        #  testing connection
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
#         sql_statement = text("SELECT * FROM patient")
        
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
