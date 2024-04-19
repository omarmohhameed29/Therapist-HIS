from fastapi import FastAPI
from . import models
from .database import engine
from .routers import patient, therapist, receptionist, session, bill, auth
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(patient.router)
app.include_router(therapist.router)
app.include_router(receptionist.router)
app.include_router(session.router)
app.include_router(bill.router)
app.include_router(auth.router)



