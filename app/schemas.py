from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime, date
from typing import Optional


class Patient(BaseModel):
    id: int
    firt_name: str
    last_name: str
    birth_date: date
    phone: str
    gender: str
    city: str

class PatientIn(Patient):
    ssn: str
    governorate: str

    class Config:
        orm_mode = True


class PatientOUT(Patient):
    ...