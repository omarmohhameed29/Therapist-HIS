from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime, date
from typing import Optional


# Class Patient(BaseException)

class PatientResponse(BaseModel):
    first_name: str
    last_name: str
    ssn: str
    birth_date: date
    gender: str
    phone: str
    city: str
    governorate: str


class PatientCreate(BaseModel):
    ssn: str
    first_name: str
    last_name: str
    birth_date: str
    gender: str
    city: str
    governorate: str
    phone: str

# Pydantic model for updating a patient


class PatientUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[str]
    gender: Optional[str]
    city: Optional[str]


class TherapistCreate(BaseModel):
    first_name: str
    last_name: str
    SSN: str
    birth_date: str
    gender: str
    city: str
    government: str
    phone: str
    specialization: str
    email: EmailStr
    password: str
    hour_rate: float


class TherapistResponse(BaseModel):
    first_name: str
    last_name: str
    phone: str
    specialization: str
    hour_rate: float


class TherapistUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    specialization: Optional[str]
    hour_rate: Optional[float]


class ReceptionistCreate(BaseModel):
    first_name: str
    last_name: str
    SSN: str
    birth_date: str
    gender: str
    phone: str
    email: EmailStr
    password: str


class ReceptionistResponse(BaseModel):
    first_name: str
    last_name: str
    phone: str


class ReceptionistUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
