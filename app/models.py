from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE, NUMERIC

from .database import Base


class Patient(Base):
    __tablename__ = "patient"

    patient_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    ssn = Column(String, unique=True)
    phone = Column(String, unique=True)
    birth_date = Column(DATE, nullable=False)
    gender = Column(String, nullable=False)
    city = Column(String, nullable=False)
    governorate = Column(String, nullable=False)


class Receptionist(Base):
    __tablename__ = "receptionist"

    receptionist_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    SSN = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    birth_date = Column(DATE)
    gender = Column(String)
    email = Column(String)
    password = Column(String)


class Therapist(Base):
    __tablename__ = "therapist"

    therapist_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    SSN = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    birth_date = Column(DATE)
    gender = Column(String)
    specialization = Column(String)
    city = Column(String)
    government = Column(String)
    email = Column(String)
    password = Column(String)
    hour_rate = Column(NUMERIC)


class TherapistAvailability(Base):
    __tablename__ = "therapist_availability"

    availability_id = Column(Integer, primary_key=True)
    therapist_id = Column(
        Integer, ForeignKey("therapist.therapist_id", ondelete="CASCADE")
    )
    date = Column(DATE)
    start = Column(String)
    end = Column(String)
    status = Column(String)


class Appointment(Base):
    __tablename__ = "appointment"

    appointment_id = Column(Integer, primary_key=True)
    therapist_id = Column(
        Integer, ForeignKey("therapist.therapist_id", ondelete="CASCADE")
    )
    patient_id = Column(Integer, ForeignKey("patient.patient_id", ondelete="CASCADE"))
    date = Column(DATE)
    start = Column(String)
    end = Column(String)


class Session(Base):
    __tablename__ = "session"

    session_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.patient_id", ondelete="CASCADE"))
    therapist_id = Column(Integer, ForeignKey("therapist.therapist_id", ondelete="CASCADE"))
    duration = Column(NUMERIC)
    date_time = Column(DateTime)
    notes = Column(String)
    session_complete = Column(Boolean)


class Bill(Base):
    __tablename__ = "bill"

    bill_id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer, ForeignKey("session.session_id", ondelete="CASCADE")
    )
    payment_status = Column(String)
    issue_date_time = Column(DateTime)
    amount = Column(NUMERIC)
    payment_method = Column(String)
