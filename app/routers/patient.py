from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import engine, get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix='/patient',
    tags=['Patient']
)


@router.get('/', response_model=List[schemas.Patient])
def get_posts(db: Session = Depends(get_db)):
    result = db.query(models.Patient).all()
    return result