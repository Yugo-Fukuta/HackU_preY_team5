from fastapi import Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from database import get_db, SessionLocal
from models.oshido import OshidoModel
from models.nickname import NicknameModel

def read_nickname(db_session: Session, uid: str):
    return db_session.query(NicknameModel).filter(NicknameModel.uid == uid).first()

def read_leaderlist(db_session: Session, celeb_name: str):
    return db_session.query(OshidoModel).filter(OshidoModel.celeb_name == celeb_name).order_by(desc(OshidoModel.oshido)).all() 

def read_lboard(celeb_name: str, maxResults: int, db: Session = Depends(get_db)): 
    leads = read_leaderlist(db, celeb_name)  
    res =[]
    i=0
    for l in leads:
        if i <= maxResults - 1:
            nick = read_nickname(db, l.uid)
            if nick != None:
                res.append({"nickName": 'ゲストさん' + str(nick.id), "oshido": l.oshido})
            else:
                break
            i+=1
        else:
            break
    return res

router = APIRouter()

@router.get("/get_leaderboard/")
def get_lboard(celeb_name: str, maxResults: int, db: Session = Depends(get_db)):
    return read_lboard(celeb_name, maxResults, db)