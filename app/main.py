from fastapi import FastAPI
from . import models
from .database import engine
from .routers import patient, therapist, receptionist

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(patient.router)
app.include_router(therapist.router)
app.include_router(receptionist.router)

