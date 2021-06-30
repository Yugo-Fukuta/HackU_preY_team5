from fastapi import Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from database import get_db, SessionLocal
from models.trend import TrendModel

def read_trend(maxResults: int, db_session: Session):
    trends = db_session.query(TrendModel).order_by(desc(TrendModel.count)).all()
    res =[]
    i=0
    for t in trends:
        if i <= maxResults - 1:
            res.append(t.celeb_name)
            i+=1
        else:
            break
    return res

router = APIRouter()

@router.get("/get_trend/")
def get_trend(maxResults: int, db: Session = Depends(get_db)):
    return read_trend(maxResults, db)