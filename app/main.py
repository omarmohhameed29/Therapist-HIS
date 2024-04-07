from fastapi import FastAPI, Depends
from . import models
from .database import engine, SessionLocal, get_db
from .routers import patient

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello World"}



@app.get("/sqltest")
def test_patients(db: SessionLocal = Depends(get_db)):
    return {"status": "success"}

