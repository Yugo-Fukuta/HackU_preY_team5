from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from database import get_db, SessionLocal
from models.news import NewsModel
from sqlalchemy.sql.expression import func, select
from apis.api_components.news_search import News_Search_Instance

class NewsSchema(BaseModel):
    whose: str
    nankome: int
    api_key: str

#その人のAPIキー一覧
def read_news_key_list(db_session: Session, whose: str):
    return db_session.query(NewsModel).filter(NewsModel.whose == whose).all()

#その人の指定個目のAPIキーの行
def read_news_row(db_session: Session, whose: str, nankome: int):
    return db_session.query(NewsModel).filter(NewsModel.whose == whose, NewsModel.nankome==nankome).first()

#APIキーの取得(テーブルの１行目)
def read_news_key(db_session: Session):
    return db_session.query(NewsModel).first().api_key

router = APIRouter()

# Newsからデータ取得
@router.get("/get_news_data/")
def get_news_data(q: str, db: Session = Depends(get_db)):
    res = News_Search_Instance(read_news_key(db)).news_search(q)
    return res, 200

#その人のAPIキー一覧
@router.get("/get_news_key_list/")
def get_news_key_list(whose: str, db: Session = Depends(get_db)):
    res = read_news_key_list(db, whose)
    return res, 200

# APIキーを登録
@router.post("/register_news_key/")
async def register_news_key(data: NewsSchema,  db: Session = Depends(get_db)):
    req = NewsModel(whose=data.whose, nankome=data.nankome, api_key=data.api_key)
    db.add(req)
    db.commit()
    res = read_news_row(db, data.whose, data.nankome)
    return res, 201

# APIキーを更新
@router.put("/update_news_key/")
async def update_news_key(data: NewsSchema, db: Session = Depends(get_db)):
    req = read_news_row(db, data.whose, data.nankome)
    req.api_key = data.api_key
    db.commit()
    return None, 204

# APIキーを削除
@router.delete("/delete_news_key/")
async def delete_news_key(whose: str, nankome: int, db: Session = Depends(get_db)):
    req = read_news_row(db, whose, nankome)
    db.delete(req)
    db.commit()
    return None, 204
