from fastapi import FastAPI, Depends
from . import models
from .database import engine, SessionLocal, get_db
from .schemas import PatientResponse, PatientCreate
# from .routers import patient

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello World"}


@app.post("/patients")
def create_patient(patient_data: PatientCreate, db: SessionLocal = Depends(get_db)):
    db_item = models.Patient(**patient_data.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



@app.get('/patients', response_model=list[PatientResponse])
def get_posts(db: SessionLocal = Depends(get_db)):
    result = db.query(models.Patient).all()
    return result

