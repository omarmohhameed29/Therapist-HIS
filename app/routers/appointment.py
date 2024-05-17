from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import and_
from .. import models, schemas
from ..database import engine, SessionLocal, get_db
from ..exceptions import NotFoundException, BadRequestException

router = APIRouter(tags=["Appointment"])


@router.get("/appointments", response_model=list[schemas.AppointmentResponse])
def get_appointments(db: SessionLocal = Depends(get_db)):
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

    # Check if there's already an appointment for the same therapist and patient on the same day
    existing_appointment = (
        db.query(models.Appointment)
        .filter(
            and_(
                models.Appointment.therapist_id == appointment_data.therapist_id,
                models.Appointment.patient_id == appointment_data.patient_id,
                models.Appointment.date == appointment_data.date,
                models.Appointment.start == appointment_data.start,
                models.Appointment.end == appointment_data.end,
            )
        )
        .first()
    )
    if existing_appointment:
        raise BadRequestException(
            detail="An appointment already exists for the same therapist, patient, and time range."
        )

    db_appointment = models.Appointment(**appointment_data.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: SessionLocal = Depends(get_db)):
    # Check if the appointment exists
    existing_appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.appointment_id == appointment_id)
        .first()
    )
    if not existing_appointment:
        raise NotFoundException(detail="Appointment ID not found.")

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
    # Check if the appointment exists
    existing_appointment = (
        db.query(models.Appointment)
        .filter(models.Appointment.appointment_id == appointment_id)
        .first()
    )
    if not existing_appointment:
        raise NotFoundException(detail="Appointment ID not found.")

    # Check if the therapist ID exists if provided
    if appointment_data.therapist_id:
        existing_therapist = (
            db.query(models.Therapist)
            .filter(models.Therapist.therapist_id == appointment_data.therapist_id)
            .first()
        )
        if not existing_therapist:
            raise NotFoundException(detail="Therapist ID not found.")

    # Check if the patient ID exists if provided
    if appointment_data.patient_id:
        existing_patient = (
            db.query(models.Patient)
            .filter(models.Patient.patient_id == appointment_data.patient_id)
            .first()
        )
        if not existing_patient:
            raise NotFoundException(detail="Patient ID not found.")

    for field, value in appointment_data.dict(exclude_unset=True).items():
        setattr(existing_appointment, field, value)

    db.commit()
    db.refresh(existing_appointment)
    return existing_appointment
