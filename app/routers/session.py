from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    tags=['Session']
)


@router.post("/session", response_model=schemas.Session)
def create_session(session: schemas.SessionCreate, db: SessionLocal = Depends(get_db)):
    db_session = SessionLocal()
    db_session.add(models.Session(**session.dict()))
    db_session.commit()
    db_session.refresh(session)
    return session
