from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import engine, SessionLocal, get_db
from ..exceptions import NotFoundException, BadRequestException
from sqlalchemy import and_


router = APIRouter(tags=["Appointment"])


@router.get("/appointments", response_model=list[schemas.AppointmentResponse])
def get_appointment(db: SessionLocal = Depends(get_db)):
    result = db.query(models.Appointment).all()
    return result


@router.post(
    "/appointments", response_model=schemas.AppointmentResponse, status_code=201
)
def create_appointment(
    appointment_data: schemas.AppointmentCreate, db: SessionLocal = Depends(get_db)
):

    # Check if the therapist ID exists
    existing_therapist = (
        db.query(models.Therapist)
        .filter(models.Therapist.therapist_id == appointment_data.therapist_id)
        .first()
    )
    if not existing_therapist:
        raise NotFoundException(detail="Therapist ID not found.")

    # Check if the patient ID exists
    existing_patient = (
        db.query(models.Patient)
        .filter(models.Patient.patient_id == appointment_data.patient_id)
        .first()
    )
    if not existing_patient:
        raise NotFoundException(detail="Patient ID not found.")

    # Check if the receptionist ID exists
    existing_receptionist = (
        db.query(models.Receptionist)
        .filter(models.Receptionist.receptionist_id == appointment_data.issued_by)
        .first()
    )
    if not existing_receptionist:
        raise NotFoundException(detail="Receptionist ID not found.")

    # Check if there's already an appointment for the same therapist and patient on the same day
    # Check if there's already an appointment with the same therapist ID, patient ID, type, and date/time
    existing_appointment = (
        db.query(models.Appointment)
        .filter(
            and_(
                models.Appointment.therapist_id == appointment_data.therapist_id,
                models.Appointment.patient_id == appointment_data.patient_id,
                models.Appointment.type == appointment_data.type,
                models.Appointment.date_and_time == appointment_data.date_and_time,
            )
        )
        .first()
    )
    if existing_appointment:
        raise BadRequestException(
            detail="An appointment already exists for the same therapist, patient, type, and date/time."
        )

    # Create and add the new appointment
    db_appointment = models.Appointment(**appointment_data.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    return db_appointment


@router.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: SessionLocal = Depends(get_db)):
    # Check if the session exists
    existing_appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.appointment_id == appointment_id)
        .first()
    )
    if not existing_appointment:
        raise NotFoundException(detail="Appointment ID not found.")

    # Delete the session
    db.delete(existing_appointment)
    db.commit()

    return {"message": "Appointment deleted successfully."}


@router.put(
    "/appointments/{appointment_id}", response_model=schemas.AppointmentResponse
)
def update_appointment(
    appointment_id: int,
    appointment_data: schemas.AppointmentUpdate,
    db: SessionLocal = Depends(get_db),
):
    # Check if the session exists
    existing_appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.appointment_id == appointment_id)
        .first()
    )
    if not existing_appointment:
        raise NotFoundException(detail="Appointment ID not found.")

    existing_therapist = (
        db.query(models.Therapist)
        .filter(models.Therapist.therapist_id == appointment_data.therapist_id)
        .first()
    )
    if not existing_therapist:
        raise NotFoundException(detail="Therapist ID not found.")

    existing_patient = (
        db.query(models.Patient)
        .filter(models.Patient.patient_id == appointment_data.patient_id)
        .first()
    )
    if not existing_patient:
        raise NotFoundException(detail="Patient ID not found.")

    existing_receptionist = (
        db.query(models.Receptionist)
        .filter(models.Receptionist.receptionist_id == appointment_data.issued_by)
        .first()
    )
    if not existing_receptionist:
        raise NotFoundException(detail="Receptionist ID not found.")

    # Update session data
    for field, value in appointment_data.dict(exclude_unset=True).items():
        setattr(existing_appointment, field, value)

    db.commit()
    db.refresh(existing_appointment)
    return existing_appointment
