from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from datetime import datetime
from typing import Optional, List
from .. import models, schemas
from ..database import engine, SessionLocal, get_db
from ..exceptions import NotFoundException, BadRequestException
from sqlalchemy import and_  # Import and_ function


router = APIRouter(tags=["Therapist Availability"])


@router.get(
    "/availabilities", response_model=list[schemas.TherapistAvailabilityResponse]
)
def get_availability(db: SessionLocal = Depends(get_db)):
    result = db.query(models.TherapistAvailability).all()
    return result


@router.post(
    "/availabilities",
    response_model=schemas.TherapistAvailabilityResponse,
    status_code=201,
)
def create_availability(
    availability_data: schemas.TherapistAvailabilityCreate,
    db: SessionLocal = Depends(get_db),
):
    # Check if therapist exists
    existing_therapist = (
        db.query(models.Therapist)
        .filter(models.Therapist.therapist_id == availability_data.therapist_id)
        .first()
    )
    if not existing_therapist:
        raise NotFoundException(detail="Therapist ID not found.")

    if availability_data.start_time >= availability_data.end_time:
        raise BadRequestException(detail="Start time must be before end time.")

    # Check if there are existing availabilities for the same therapist on the same day
    existing_availabilities = (
        db.query(models.TherapistAvailability)
        .filter(
            models.TherapistAvailability.therapist_id == availability_data.therapist_id,
            models.TherapistAvailability.date == availability_data.date,
            # Check for overlapping time ranges
            and_(
                models.TherapistAvailability.start_time < availability_data.end_time,
                models.TherapistAvailability.end_time > availability_data.start_time,
            ),
        )
        .all()
    )

    if existing_availabilities:
        raise BadRequestException(
            detail="Availability already exists for the same therapist on the same day and time range."
        )

    # Create TherapistAvailability instance
    db_availability = models.TherapistAvailability(**availability_data.dict())

    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability


@router.delete("/availabilities/{availability_id}")
def delete_availability(availability_id: int, db: SessionLocal = Depends(get_db)):
    # Check if the session exists
    existing_availability = (
        db.query(models.TherapistAvailability)
        .filter(models.TherapistAvailability.availability_id == availability_id)
        .first()
    )
    if not existing_availability:
        raise NotFoundException(detail="Therapist Availability ID not found.")

    # Delete the session
    db.delete(existing_availability)
    db.commit()

    return {"message": "therapist availability deleted successfully."}


@router.put(
    "/availabilities/{availability_id}",
    response_model=schemas.TherapistAvailabilityResponse,
)
def update_availability(
    availability_id: int,
    availability_data: schemas.TherapistAvailabilityUpdate,
    db: SessionLocal = Depends(get_db),
):
    # Check if the availability exists
    existing_availability = (
        db.query(models.TherapistAvailability)
        .filter(models.TherapistAvailability.availability_id == availability_id)
        .first()
    )
    if not existing_availability:
        raise NotFoundException(detail="Therapist Availability ID not found.")

    # Validate start_time is before end_time in the updated data
    if (
        availability_data.start_time is not None
        and availability_data.end_time is not None
        and availability_data.start_time >= availability_data.end_time
    ):
        raise BadRequestException(detail="Start time must be before end time.")

    # Check for conflicting availabilities
    if (
        availability_data.date
        or availability_data.start_time
        or availability_data.end_time
    ):
        conflicting_availability = (
            db.query(models.TherapistAvailability)
            .filter(
                models.TherapistAvailability.therapist_id
                == existing_availability.therapist_id,
                models.TherapistAvailability.availability_id != availability_id,
                # Check for overlapping time ranges
                and_(
                    (
                        models.TherapistAvailability.date == availability_data.date
                        if availability_data.date
                        else True
                    ),
                    (
                        models.TherapistAvailability.start_time
                        < availability_data.end_time
                        if availability_data.end_time
                        else True
                    ),
                    (
                        models.TherapistAvailability.end_time
                        > availability_data.start_time
                        if availability_data.start_time
                        else True
                    ),
                ),
            )
            .first()
        )
        if conflicting_availability:
            raise BadRequestException(
                detail="Conflicting availability for the new date and time range."
            )

    # Update availability data
    for field, value in availability_data.dict(exclude_unset=True).items():
        if field == "status":
            # If status is not provided or has an invalid value, default to "Available"
            value = value if value in ["Available", "Unavailable"] else "Available"
        setattr(existing_availability, field, value)

    db.commit()
    db.refresh(existing_availability)
    return existing_availability
