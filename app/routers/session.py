from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    tags=['Session']
)


@router.get('/sessions', response_model=list[schemas.SessionResponse])
def get_therapists(db: SessionLocal = Depends(get_db)):
    result = db.query(models.Session).all()
    return result

@router.post("/sessions", response_model=schemas.SessionResponse, status_code=201)
def create_therapist(sessoin_data: schemas.SessionCreate, db: SessionLocal = Depends(get_db)):
    db_session = models.Session(**sessoin_data.model_dump())

    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


@router.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: SessionLocal = Depends(get_db)):
    # Check if the session exists
    existing_session = db.query(models.Session).filter(models.Session.session_id == session_id).first()
    if existing_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Exists")


    # Delete the session
    db.delete(existing_session)
    db.commit()

    return {"message": "session deleted successfully"}


@router.put("/sessions/{session_id}", response_model=schemas.SessionResponse)
def update_session(session_id: int, session_data: schemas.SessionUpdate, db: SessionLocal = Depends(get_db)):
    # Check if the session exists
    existing_session = db.query(models.Session).filter(models.Session.session_id == session_id).first()
    if existing_session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # Update session data
    for field, value in session_data.dict(exclude_unset=True).items():
        setattr(existing_session, field, value)

    db.commit()
    db.refresh(existing_session)
    return existing_session
