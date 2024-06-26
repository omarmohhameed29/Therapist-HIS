from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    tags=['Patients']
)


@router.post("/patients", response_model=schemas.PatientResponse)
def create_patient(patient_data: schemas.PatientCreate, db: SessionLocal = Depends(get_db)):
    db_item = models.Patient(**patient_data.model_dump())

    existing_patient_with_ssn = db.query(models.Patient).filter(
        models.Patient.ssn == db_item.ssn).first()
    existing_patient_with_phone = db.query(models.Patient).filter(
        models.Patient.phone == db_item.phone).first()

    if existing_patient_with_ssn:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="SSN already exists")
    if existing_patient_with_phone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Phone already exists")

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get('/patients', response_model=list[schemas.PatientResponse])
def get_posts(db: SessionLocal = Depends(get_db)):
    result = db.query(models.Patient).all()
    return result


@router.get("/patients/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(patient_id: int, db: SessionLocal = Depends(get_db)):
    existing_patient = db.query(models.Patient).filter(
        models.Patient.patient_id == patient_id).first()
    if existing_patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")
    return existing_patient


@router.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient_data: schemas.PatientUpdate, db: SessionLocal = Depends(get_db)):
    # Check if the patient exists
    existing_patient = db.query(models.Patient).filter(
        models.Patient.patient_id == patient_id).first()
    if existing_patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")

    # Update the patient data
    for field, value in patient_data.dict().items():
        setattr(existing_patient, field, value)

    db.commit()
    db.refresh(existing_patient)
    return {"Data": existing_patient}


@router.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: SessionLocal = Depends(get_db)):
    # Check if the patient exists
    existing_patient = db.query(models.Patient).filter(
        models.Patient.patient_id == patient_id).first()
    if existing_patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")

    # Delete the patient
    db.delete(existing_patient)
    db.commit()

    return {"message": "Patient deleted successfully"}
