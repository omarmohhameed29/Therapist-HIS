from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    tags=['Receptionist']
)


@router.get('/receptionists', response_model=list[schemas.ReceptionistResponse])
def get_receptionists(db: SessionLocal = Depends(get_db)):
    result = db.query(models.Receptionist).all()
    return result

@router.post("/receptionists", response_model=schemas.ReceptionistResponse, status_code=201)
def create_receptionist(receptionist_data: schemas.ReceptionistCreate, db: SessionLocal = Depends(get_db)):
    db_receptionist_data = models.Receptionist(**receptionist_data.model_dump())
    db.add(db_receptionist_data)
    db.commit()
    db.refresh(db_receptionist_data)
    return db_receptionist_data


@router.delete("/receptionists/{receptionist_id}")
def delete_receptionist(receptionist_id: int, db: SessionLocal = Depends(get_db)):
    # Check if the patient exists
    existing_receptionist = db.query(models.Receptionist).filter(models.Receptionist.receptionist_id == receptionist_id).first()
    if existing_receptionist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")


    # Delete the patient
    db.delete(existing_receptionist)
    db.commit()

    return {"message": "receptionist deleted successfully"}


@router.put("/receptionists/{receptionist_id}", response_model=schemas.ReceptionistResponse)
def update_receptionist(receptionist_id: int, receptionist_data: schemas.ReceptionistUpdate, db: SessionLocal = Depends(get_db)):
    # Check if the therapist exists
    existing_receptionist = db.query(models.Receptionist).filter(models.Receptionist.receptionist_id == receptionist_id).first()
    if existing_receptionist is None:
        raise HTTPException(status_code=404, detail="Receptionist not found")

    # Update the therapist data
    for field, value in receptionist_data.dict(exclude_unset=True).items():
        setattr(existing_receptionist, field, value)

    db.commit()
    db.refresh(existing_receptionist)
    return existing_receptionist
