from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime, date
from typing import Optional


class PatientResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: str 
    sex: str
    city: str


class PatientCreate(BaseModel):
    ssn: str
    first_name: str
    last_name: str
    birth_date: str
    sex: str
    city: str
    governorate: str
    phone: str