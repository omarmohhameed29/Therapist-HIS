from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    tags=['Therapists']
)


@router.get('/therapists', response_model=list[schemas.TherapistResponse])
def get_therapists(db: SessionLocal = Depends(get_db)):
    result = db.query(models.Therapist).all()
    return result


@router.get("/therapists/{therapist_id}", response_model=schemas.TherapistResponse)
def get_therapist(therapist_id: int, db: SessionLocal = Depends(get_db)):
    existing_therapist = db.query(models.Therapist).filter(
        models.Therapist.therapist_id == therapist_id).first()
    if existing_therapist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")
    return existing_therapist


@router.post("/therapists", response_model=schemas.TherapistResponse, status_code=201)
def create_therapist(therapist_data: schemas.TherapistCreate, db: SessionLocal = Depends(get_db)):
    db_therapist = models.Therapist(**therapist_data.model_dump())
    existing_therapist_with_ssn = db.query(models.Therapist).filter(
        models.Therapist.SSN == therapist_data.SSN).first()
    existing_therapist_with_phone = db.query(models.Therapist).filter(
        models.Therapist.phone == therapist_data.phone).first()

    if existing_therapist_with_ssn:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="SSN already exists")
    if existing_therapist_with_phone:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Phone already exists")

    db.add(db_therapist)
    db.commit()
    db.refresh(db_therapist)
    return db_therapist


@router.delete("/therapists/{therapist_id}")
def delete_therapist(therapist_id: int, db: SessionLocal = Depends(get_db)):
    # Check if the therapist exists
    existing_therapist = db.query(models.Therapist).filter(
        models.Therapist.therapist_id == therapist_id).first()
    if existing_therapist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")

    # Delete the therapist
    db.delete(existing_therapist)
    db.commit()

    return {"message": "therapist deleted successfully"}


@router.put("/therapists/{therapist_id}", response_model=schemas.TherapistResponse)
def update_therapist(therapist_id: int, therapist_data: schemas.TherapistUpdate, db: SessionLocal = Depends(get_db)):
    # Check if the therapist exists
    existing_therapist = db.query(models.Therapist).filter(
        models.Therapist.therapist_id == therapist_id).first()
    if existing_therapist is None:
        raise HTTPException(status_code=404, detail="Therapist not found")

    # Update the therapist data
    for field, value in therapist_data.dict(exclude_unset=True).items():
        setattr(existing_therapist, field, value)

    db.commit()
    db.refresh(existing_therapist)
    return existing_therapist
