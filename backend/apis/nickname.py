from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from database import get_db, SessionLocal
from models.nickname import NicknameModel

class NicknameSchema(BaseModel):
    uid: str

def read_nickname(db_session: Session, uid: str):
    return db_session.query(NicknameModel).filter(NicknameModel.uid == uid).first()

router = APIRouter()

@router.get("/get_nickname/")
def get_nickname(uid: str, db: Session = Depends(get_db)):
    res = 'ゲストさん' + str(read_nickname(db, uid).id)
    return res, 200

@router.post("/register_nickname/")
async def create_nickname(data: NicknameSchema, db: Session = Depends(get_db)):
    req = NicknameModel(uid=data.uid)
    db.add(req)
    db.commit()
    res = 'ゲストさん' + str(read_nickname(db, data.uid).id)
    return res, 201

"""
@router.put("/update_nickname/")
async def update_oshido(data: NicknameSchema, db: Session = Depends(get_db)):
    req = read_nickname(db, data.uid)
    req.nickname = data.nickname
    db.commit()
    return None, 204
"""

@router.delete("/delete_nickname/")
async def delete_nickname(uid: str, db: Session = Depends(get_db)):
    req = read_nickname(db, uid)
    db.delete(req)
    db.commit()
    return None, 204