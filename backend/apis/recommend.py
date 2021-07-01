from fastapi import Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from database import get_db, SessionLocal
from models.oshido import OshidoModel
from models.recommend import RecommendModel
import datetime
import pandas as pd
import pandas.tseries.offsets as offsets

# 指定したuidの最推し
def read_uid_saioshi(db_session: Session, uid: str):
    return db_session.query(OshidoModel).filter(OshidoModel.uid == uid).order_by(desc(OshidoModel.oshido)).first().celeb_name

#指定した有名人を推しているuidのデータ一覧(自分以外)
def read_celeb_followers(db_session: Session, uid: str, celeb_name: str):
    return db_session.query(OshidoModel).filter(OshidoModel.uid != uid, OshidoModel.celeb_name == celeb_name).order_by(desc(OshidoModel.oshido)).all()

#Recommend用。そのuidのデータの中で、指定した有名人以外で推し度が最も高い有名人を抽出
def generate_recommend(db_session: Session, uid: str, celeb_name: str):
    return db_session.query(OshidoModel).filter(OshidoModel.uid == uid, OshidoModel.celeb_name != celeb_name).order_by(desc(OshidoModel.oshido)).first()

def read_recommend(db_session: Session, uid: str):
    return db_session.query(RecommendModel).filter(RecommendModel.uid == uid).first()

router = APIRouter()

#Recommend抽出
@router.get("/get_recommend/")
def get_recommend_data(uid: str, db: Session = Depends(get_db)):
    '''
    uid入力 -> そのuidの最推しの有名人を検索 -> その有名人の推し度が最も高いuidを検索 -> そのuidの最推しの有名人を検索 -> その有名人がレコメンドされる。
    backend/seed/seed_uid_v1.pyというuidのseedファイルを適当に作ったので、適宜内容変更してください。
    '''
    rec = read_recommend(db, uid)
    put_flag = False
    if rec != None:
        cached_time = rec.updated_at
        current_time = datetime.datetime.utcnow()+ datetime.timedelta(hours=9)
        if pd.Timestamp(current_time.replace(microsecond = 0)) < cached_time+offsets.Hour(3):
            return rec.recommend
        else:
            put_flag = True
    celeb_name = read_uid_saioshi(db, uid)
    celeb_followers = read_celeb_followers(db, uid, celeb_name)
    for c in celeb_followers:
        res = generate_recommend(db, c.uid, celeb_name)
        if res != None:
            if put_flag:
                rec.recommend = res.celeb_name
                db.commit()
                return res.celeb_name, 200
            else:
                req = RecommendModel(uid = uid, recommend = res.celeb_name)
                db.add(req)
                db.commit()
                return res.celeb_name, 200
    return None, 200