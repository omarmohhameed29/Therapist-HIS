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
    sex: str
    phone: str


class PatientCreate(BaseModel):
    ssn: str
    first_name: str
    last_name: str
    birth_date: str
    sex: str
    city: str
    governorate: str
    phone: str

# Pydantic model for updating a patient
class PatientUpdate(BaseModel):
    first_name: str
    last_name: str
    birth_date: str
    sex: str
    city: str