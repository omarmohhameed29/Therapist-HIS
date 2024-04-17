from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    tags=['Bill']
)


@router.get('/bills', response_model=list[schemas.BillResponse])
def get_therapists(db: SessionLocal = Depends(get_db)):
    result = db.query(models.Bill).all()
    return result

@router.post("/bills", response_model=schemas.BillResponse, status_code=201)
def create_therapist(bill_data: schemas.BillCreate, db: SessionLocal = Depends(get_db)):
    db_bill = models.Bill(**bill_data.model_dump())

    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill


@router.delete("/bills/{bill_id}")
def delete_session(bill_id: int, db: SessionLocal = Depends(get_db)):
    # Check if the bill exists
    existing_bill = db.query(models.Bill).filter(models.Bill.bill_id == bill_id).first()
    if existing_bill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")


    # Delete the bill
    db.delete(existing_bill)
    db.commit()

    return {"message": "bill deleted successfully"}


@router.put("/bills/{bill_id}", response_model=schemas.BillResponse)
def update_session(bill_id: int, bill_data: schemas.BillUpdate, db: SessionLocal = Depends(get_db)):
    # Check if the bill exists
    existing_bill = db.query(models.Bill).filter(models.Bill.bill_id == bill_id).first()
    if existing_bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")

    # Update bill data
    for field, value in bill_data.dict(exclude_unset=True).items():
        setattr(existing_bill, field, value)

    db.commit()
    db.refresh(existing_bill)
    return existing_bill
