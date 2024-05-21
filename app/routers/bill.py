from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import engine, SessionLocal, get_db
from datetime import datetime

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
    Therapist = models.Therapist
    Patient = models.Patient

    # Query bills along with associated session, appointment, therapist, and patient information
    query = db.query(Bill.bill_id, Patient.first_name, Patient.last_name,
                     Therapist.first_name, Therapist.last_name,
                     Bill.amount, Bill.payment_status, Bill.issue_date_time, Bill.payment_method, SessionModel.session_id, Therapist.specialization).\
        join(SessionModel, Bill.session_id == SessionModel.session_id).\
        join(Therapist, SessionModel.therapist_id == Therapist.therapist_id).\
        join(Patient, SessionModel.patient_id == Patient.patient_id).\
        order_by(Bill.issue_date_time.desc())

    # Execute the query and fetch the result
    result = query.all()
    print(result)
    # Extract amount and issue_date_time from the result without their data types
    extracted_data = []
    for row in result:
        data_without_amount_issue = {
            "id": row[0],
            "patient": row[1] + ' ' + row[2],
            "doctor": row[3] + ' ' + row[4],
            "specialization": row[10],
            "status": row[6],
            "paymentMethod": row[8]
        }
        data_without_amount_issue["amount"] = row[5]  # Add amount separately
        # Add issue_date_time separately
        data_without_amount_issue["paymentDate"] = row[7]
        # Add issue_date_time separately
        data_without_amount_issue["session_id"] = row[9]

        extracted_data.append(data_without_amount_issue)
    print(extracted_data)
    return extracted_data


@router.post("/bills", response_model=schemas.BillResponse, status_code=201)
def create_bill(bill_data: schemas.BillCreate, db: SessionLocal = Depends(get_db)):
    db_bill = models.Bill(**bill_data.model_dump())
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill


@router.post('/bills/{session_id}')
def generate_bill_from_session_id(session_id: int, db: SessionLocal = Depends(get_db)):
    """
    Generate a bill from a given session_id.
    """
    # Define aliases for the tables
    SessionModel = models.Session
    Therapist = models.Therapist
    Patient = models.Patient

    # Query the session information
    session = db.query(SessionModel).filter(
        SessionModel.session_id == session_id).first()
    session.session_complete = True
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Query the related therapist and patient information
    therapist = db.query(Therapist).filter(
        Therapist.therapist_id == session.therapist_id).first()
    patient = db.query(Patient).filter(
        Patient.patient_id == session.patient_id).first()

    if not therapist or not patient:
        raise HTTPException(
            status_code=404, detail="Therapist or Patient not found")

    # Create a new Bill instance
    new_bill = models.Bill(
        session_id=session.session_id,
        payment_status="Pending",  # Default status
        issue_date_time=datetime.now(),  # Current time as issue date
        # Assuming therapist has hour_rate and session has duration attributes
        amount=therapist.hour_rate * session.duration,
        payment_method="Cash",  # Default payment method
    )

    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)

    return new_bill


@router.delete("/bills/{bill_id}")
def delete_bill(bill_id: int, db: SessionLocal = Depends(get_db)):
    # Check if the bill exists
    existing_bill = db.query(models.Bill).filter(
        models.Bill.bill_id == bill_id).first()
    if existing_bill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")
    # Delete the bill
    db.delete(existing_bill)
    db.commit()

    return {"message": "bill deleted successfully"}


@router.put("/bills/{bill_id}", response_model=schemas.BillResponse)
def update_bill(bill_id: int, bill_data: schemas.BillUpdate, db: SessionLocal = Depends(get_db)):
    # Check if the bill exists
    existing_bill = db.query(models.Bill).filter(
        models.Bill.bill_id == bill_id).first()
    if existing_bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")

    # Update bill data
    for field, value in bill_data.dict(exclude_unset=True).items():
        setattr(existing_bill, field, value)

    db.commit()
    db.refresh(existing_bill)
    return existing_bill
