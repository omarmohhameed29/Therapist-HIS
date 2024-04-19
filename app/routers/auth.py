from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import models, schemas, utils, oauth2
from ..database import engine, SessionLocal, get_db

router  = APIRouter()


# def login(user_credentials: schemas.UserLogin, db: SessionLocal):

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: SessionLocal=Depends(get_db)):

    if (user_credentials.role == 'Therapist'):
        user = db.query(models.Therapist).filter(models.Therapist.email == user_credentials.email).first()

        if user:
            if not utils.verify(user_credentials.password, user.password):
                raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
        else : raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials") # valid user wrong role
        
        # Create a token 
        access_token = oauth2.create_access_token(data = {"user_id": user.therapist_id}) 


    elif (user_credentials.role == 'Receptionist'):
        user = db.query(models.Receptionist).filter(models.Receptionist.email == user_credentials.email).first()

        if user:
            if not utils.verify(user_credentials.password, user.password):
                raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials") # Wrong pass

        else : raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials") # Valid user wrong role
        
        # Create a token 
        access_token = oauth2.create_access_token(data = {"user_id": user.receptionist_id}) # Valid user valid role

    # Invalid Role  
    else : raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Invalid role")


    # Return token 
    return {"access_token" : access_token, "token_type":"bearer"}
