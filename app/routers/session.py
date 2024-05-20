from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    tags=['Session']
)

@router.get("/session")
def get_sessions(db: SessionLocal = Depends(get_db)):
    # Define aliases for the tables
    SessionModel = models.Session
    Appointment = models.Appointment
    Therapist = models.Therapist
    Patient = models.Patient

    # Query bills along with associated session, appointment, therapist, and patient information
    query = db.query(Patient.first_name, Patient.last_name,
                     Therapist.first_name, Therapist.last_name,
                     SessionModel.session_id, SessionModel.notes, SessionModel.duration, SessionModel.date_time) .\
        join(Therapist, SessionModel.therapist_id == Therapist.therapist_id).\
        join(Patient, SessionModel.patient_id == Patient.patient_id)

    # Execute the query and fetch the result
    result = query.all()
    print(result)
    # Extract amount and issue_date_time from the result without their data types
    extracted_data = []
    for row in result:
        data_without_amount_issue = {
            "patient_name": row[0] + ' ' +row[1],
            "therapist_name": row[2] + ' ' + row[3],
        }
        data_without_amount_issue["session_id"] = row[4]  # Add amount separately
        data_without_amount_issue["notes"] = row[5]  # Add issue_date_time separately
        data_without_amount_issue["duration"] = row[6]  
        data_without_amount_issue["date_time"] = row[7]  
        extracted_data.append(data_without_amount_issue)
    print(extracted_data)
    return extracted_data


@router.get("/session/{session_id}")
def get_session_by_id(session_id: int, db: SessionLocal = Depends(get_db)):
    # Aliases for the tables
    SessionModel = models.Session
    Therapist = models.Therapist
    Patient = models.Patient

    # Query the session along with associated therapist and patient information
    query = db.query(
        SessionModel.session_id,
        SessionModel.notes,
        SessionModel.duration,
        SessionModel.date_time,
        Patient.first_name.label('patient_first_name'),
        Patient.last_name.label('patient_last_name'),
        Therapist.first_name.label('therapist_first_name'),
        Therapist.last_name.label('therapist_last_name')
    ).join(Therapist, SessionModel.therapist_id == Therapist.therapist_id)\
     .join(Patient, SessionModel.patient_id == Patient.patient_id)\
     .filter(SessionModel.session_id == session_id)

    result = query.first()

    if not result:
        raise HTTPException(status_code=404, detail="Session not found")

    # Construct the response
    response = {
        "session_id": result.session_id,
        "notes": result.notes,
        "duration": result.duration,
        "date_time": result.date_time,
        "patient_name": f"{result.patient_first_name} {result.patient_last_name}",
        "therapist_name": f"{result.therapist_first_name} {result.therapist_last_name}"
    }

    return response


@router.get("/sessions/therapist/{therapist_id}")
def get_sessions_by_therapist_id(therapist_id: int, db: SessionLocal = Depends(get_db)):
    # Aliases for the tables
    SessionModel = models.Session
    Therapist = models.Therapist
    Patient = models.Patient

    # Query the sessions for the given therapist along with associated patient information
    query = db.query(
        SessionModel.session_id,
        SessionModel.notes,
        SessionModel.duration,
        SessionModel.date_time,
        Patient.first_name.label('patient_first_name'),
        Patient.last_name.label('patient_last_name'),
        Therapist.first_name.label('therapist_first_name'),
        Therapist.last_name.label('therapist_last_name')
    ).join(Therapist, SessionModel.therapist_id == Therapist.therapist_id)\
     .join(Patient, SessionModel.patient_id == Patient.patient_id)\
     .filter(SessionModel.therapist_id == therapist_id)

    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="No sessions found for the given therapist")

    # Construct the response
    response = [
        {
            "session_id": result.session_id,
            "notes": result.notes,
            "duration": result.duration,
            "date_time": result.date_time,
            "patient_name": f"{result.patient_first_name} {result.patient_last_name}",
            "therapist_name": f"{result.therapist_first_name} {result.therapist_last_name}"
        } for result in results
    ]

    return response


@router.post("/session", response_model=schemas.Session)
def create_session(session: schemas.SessionCreate, db: SessionLocal = Depends(get_db)):
    db_session = models.Session(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session



@router.delete("/session/{session_id}")
def delete_session(session_id: int, db: SessionLocal = Depends(get_db)):
    # Check if the session exists
    existing_session = db.query(models.Session).filter(models.Session.session_id == session_id).first()
    if existing_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")
    # Delete the session
    db.delete(existing_session)
    db.commit()
    return {"message": "session deleted successfully"}


@router.put("/session/{session_id}", response_model=schemas.SessionResponse)
def update_session(session_id: int, session_data: schemas.SessionUpdate, db: SessionLocal = Depends(get_db)):
    # Check if the session exists
    existing_session = db.query(models.Session).filter(models.Session.session_id == session_id).first()
    if existing_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # Update session data
    for field, value in session_data.dict(exclude_unset=True).items():
        setattr(existing_session, field, value)

    db.commit()
    db.refresh(existing_session)
    return existing_session

