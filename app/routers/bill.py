from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    tags=['Bill']
)


# @router.get('/bills', response_model=list[schemas.BillResponse])
@router.get('/bills')
def get_bills_with_details(db: SessionLocal = Depends(get_db)):
    """
    Retrieves bills along with associated therapist and patient information.
    """
    # Define aliases for the tables
    Bill = models.Bill
    SessionModel = models.Session
    Appointment = models.Appointment
    Therapist = models.Therapist
    Patient = models.Patient

    # Query bills along with associated session, appointment, therapist, and patient information
    query = db.query(Bill.bill_id, Patient.first_name, Patient.last_name,
                     Therapist.first_name, Therapist.last_name,
                     Bill.amount, Bill.payment_status, Bill.issue_date_time).\
        join(SessionModel, Bill.session_id == SessionModel.session_id).\
        join(Appointment, SessionModel.appointment_id == Appointment.appointment_id).\
        join(Therapist, Appointment.therapist_id == Therapist.therapist_id).\
        join(Patient, Appointment.patient_id == Patient.patient_id)

    # Execute the query and fetch the result
    result = query.all()

    # Extract amount and issue_date_time from the result without their data types
    extracted_data = []
    for row in result:
        data_without_amount_issue = {
            "bill_id": row[0],
            "patient_first_name": row[1],
            "patient_last_name": row[2],
            "therapist_first_name": row[3],
            "therapist_last_name": row[4],
            "payment_status": row[6],
        }
        data_without_amount_issue["amount"] = row[5]  # Add amount separately
        data_without_amount_issue["issue_date_time"] = row[7]  # Add issue_date_time separately
        extracted_data.append(data_without_amount_issue)

    return extracted_data



@router.post("/bills", response_model=schemas.BillResponse, status_code=201)
def create_bill(bill_data: schemas.BillCreate, db: SessionLocal = Depends(get_db)):
    db_bill = models.Bill(**bill_data.model_dump())

    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill


@router.delete("/bills/{bill_id}")
def delete_bill(bill_id: int, db: SessionLocal = Depends(get_db)):
    # Check if the bill exists
    existing_bill = db.query(models.Bill).filter(models.Bill.bill_id == bill_id).first()
    if existing_bill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")


    # Delete the bill
    db.delete(existing_bill)
    db.commit()

    return {"message": "bill deleted successfully"}


@router.put("/bills/{bill_id}", response_model=schemas.BillResponse)
def update_bill(bill_id: int, bill_data: schemas.BillUpdate, db: SessionLocal = Depends(get_db)):
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
