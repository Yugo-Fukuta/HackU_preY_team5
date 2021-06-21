from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from database import get_db, SessionLocal
from models.oshido import OshidoModel

class OshidoSchema(BaseModel):
    uid: str
    celeb_name: str
    oshido: int

class UpdateOshidoSchema(BaseModel):
    celeb_name: str
    oshido: int

# そのuidのデータ一覧
def get_uid_data(db_session: Session, uid: str):
    return db_session.query(OshidoModel).filter(OshidoModel.uid == uid).all()

# そのuidの、その有名人に対する推し度
def get_oshido(db_session: Session, uid: str, celeb_name: str):
    return db_session.query(OshidoModel).filter(OshidoModel.uid == uid, OshidoModel.celeb_name==celeb_name).first()

router = APIRouter()

# そのuidのデータ一覧
@router.get("/show_oshido_list/{uid}")
def read_uid_data(uid: str, db: Session = Depends(get_db)):
    uid_data_list = get_uid_data(db, uid)
    return uid_data_list, 200

# そのuidの、その有名人に対する推し度
@router.get("/show_oshido/uid={uid}&celeb_name={celeb_name}")
def read_oshido(uid: str, celeb_name: str, db: Session = Depends(get_db)):
    res = get_oshido(db, uid, celeb_name)
    return res, 200

# Oshidoを登録
@router.post("/register_oshido")
async def create_oshido(data: OshidoSchema,  db: Session = Depends(get_db)):
    req = OshidoModel(uid=data.uid, celeb_name=data.celeb_name, oshido=data.oshido)
    db.add(req)
    db.commit()
    res = get_oshido(db, data.uid, data.celeb_name)
    return res, 201

# Oshidoを更新
@router.put("/update_oshido")
async def update_oshido(data: OshidoSchema, db: Session = Depends(get_db)):
    req = get_oshido(db, data.uid, data.celeb_name)
    req.oshido = data.oshido
    db.commit()
    return None, 204

# Oshidoを削除
@router.delete("/delete_oshido/uid={uid}&celeb_name={celeb_name}")
async def delete_oshido(uid: str, celeb_name: str, db: Session = Depends(get_db)):
    req = get_oshido(db, uid, celeb_name)
    db.delete(req)
    db.commit()
    return None, 204