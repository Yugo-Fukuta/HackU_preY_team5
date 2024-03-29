from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from database import get_db, SessionLocal
from models.youtube import YouTubeModel
from sqlalchemy.sql.expression import func, select
from apis.api_components.youtube_search import YouTube_Search_Instance
import random

class YouTubeSchema(BaseModel):
    whose: str
    nankome: int
    api_key: str

#その人のAPIキー一覧
def read_youtube_key_list(db_session: Session, whose: str):
    return db_session.query(YouTubeModel).filter(YouTubeModel.whose == whose).all()

#その人の指定個目のAPIキーの行
def read_youtube_row(db_session: Session, whose: str, nankome: int):
    return db_session.query(YouTubeModel).filter(YouTubeModel.whose == whose, YouTubeModel.nankome==nankome).first()

#APIキーの取得(テーブル全体からランダム)
def read_youtube_key(db_session: Session):
    return random.choice(db_session.query(YouTubeModel).all()).api_key

router = APIRouter()

# YouTubeからデータ取得
@router.get("/get_youtube_data/")
def get_youtube_data(q: str, maxResults: int, db: Session = Depends(get_db)):
    res = YouTube_Search_Instance(read_youtube_key(db)).youtube_search(q, maxResults)
    return res, 200

# 再生回数などのメタデータ取得
@router.get("/get_youtube_meta_data/")
def get_youtube_meta_data(videoIDs: str, db: Session = Depends(get_db)):
    res = YouTube_Search_Instance(read_youtube_key(db)).get_meta_data(videoIDs)
    return res, 200

# 有名人のチャンネル動画を取得
@router.get("/get_youtube_channel_data/")
def get_youtube_channel_data(q: str, maxResults: int, db: Session = Depends(get_db)):
    res = YouTube_Search_Instance(read_youtube_key(db)).get_channel_videos(q, maxResults)
    return res, 200

#その人のAPIキー一覧
@router.get("/get_youtube_key_list/")
def get_youtube_key_list(whose: str, db: Session = Depends(get_db)):
    res = read_youtube_key_list(db, whose)
    return res, 200

# APIキーを登録
@router.post("/register_youtube_key/")
async def register_youtube_key(data: YouTubeSchema,  db: Session = Depends(get_db)):
    req = YouTubeModel(whose=data.whose, nankome=data.nankome, api_key=data.api_key)
    db.add(req)
    db.commit()
    res = read_youtube_row(db, data.whose, data.nankome)
    return res, 201

# APIキーを更新
@router.put("/update_youtube_key/")
async def update_youtube_key(data: YouTubeSchema, db: Session = Depends(get_db)):
    req = read_youtube_row(db, data.whose, data.nankome)
    req.api_key = data.api_key
    db.commit()
    return None, 204

# APIキーを削除
@router.delete("/delete_youtube_key/")
async def delete_youtube_key(whose: str, nankome: int, db: Session = Depends(get_db)):
    req = read_youtube_row(db, whose, nankome)
    db.delete(req)
    db.commit()
    return None, 204