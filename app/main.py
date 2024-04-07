from fastapi import FastAPI, Depends, HTTPException, status
from . import models
from .database import engine, SessionLocal, get_db
from .schemas import PatientResponse, PatientCreate, PatientUpdate
# from .routers import patient

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hello World"}


@app.post("/patients", response_model=PatientResponse)
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


@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient_data: PatientUpdate, db: SessionLocal = Depends(get_db)):
    # Check if the patient exists
    existing_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if existing_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")
    
    # Update the patient data
    for field, value in patient_data.dict().items():
        setattr(existing_patient, field, value)
    
    db.commit()
    db.refresh(existing_patient)
    return {"Data": existing_patient}



@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: SessionLocal = Depends(get_db)):
    # Check if the patient exists
    existing_patient = db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()
    if existing_patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")


    # Delete the patient
    db.delete(existing_patient)
    db.commit()

    return {"message": "Patient deleted successfully"}

