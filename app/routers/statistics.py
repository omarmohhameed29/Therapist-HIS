from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from sqlalchemy import func
from ..database import engine, SessionLocal, get_db
from datetime import date

router = APIRouter(
    tags=['Statistics']
)

@router.get("/statistics")
def get_sessions_summary(db: SessionLocal = Depends(get_db)):
    # Aliases for the tables
    SessionModel = models.Session
    Bill = models.Bill

    # Query to count the total number of sessions
    total_sessions = db.query(func.count(SessionModel.session_id)).scalar()

    # Query to sum the total amount paid from bills
    total_amount_paid = db.query(func.sum(Bill.amount)).filter(Bill.payment_status == 'paid').scalar()

    # Query to calculate the average session duration
    average_duration = db.query(func.avg(SessionModel.duration)).scalar()

    # Query to calculate today's revenue
    today = date.today()
    todays_revenue = db.query(func.sum(Bill.amount)).filter(func.date(Bill.issue_date_time) == today).scalar()

    # Construct the response
    response = {
        "total_sessions": total_sessions,
        "total_amount_paid": total_amount_paid,
        "average_session_duration": average_duration,
        "todays_revenue": todays_revenue
    }

    return response
