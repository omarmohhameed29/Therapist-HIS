from fastapi import FastAPI
from . import models
from .database import engine
from .routers import patient, therapist

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(patient.router)
app.include_router(therapist.router)

