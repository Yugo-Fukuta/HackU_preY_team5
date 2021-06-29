from typing import Optional
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from pydantic import BaseModel
from database import get_db, SessionLocal
from models.twitter import TwitterModel
from sqlalchemy.sql.expression import func, select
from apis.api_components.twitter_search import Twitter_Search_Instance
import random

class TwitterSchema(BaseModel):
    whose: str
    nankome: int
    api_key: str
    api_key_secret: str
    access_token: str
    access_token_secret: str

#その人の認証一覧
def read_twitter_auth_list(db_session: Session, whose: str):
    return db_session.query(TwitterModel).filter(TwitterModel.whose == whose).all()

#その人の指定個目のAPIキーの行
def read_twitter_row(db_session: Session, whose: str, nankome: int):
    return db_session.query(TwitterModel).filter(TwitterModel.whose == whose, TwitterModel.nankome==nankome).first()

#認証情報の取得(テーブル全体からランダム)
def read_twitter_auth_first(db_session: Session):
    return random.choice(db_session.query(TwitterModel).all())

router = APIRouter()

# twitterからデータ取得
@router.get("/get_twitter_data/")
def get_twitter_data(q: str, maxResults: int, db: Session = Depends(get_db)):
    res = Twitter_Search_Instance(read_twitter_auth_first(db)).twitter_search(q, maxResults)
    return res, 200

@router.get("/get_celeb_tweets/")
def get_celeb_tweets(q: str, maxResults: Optional[int] = 5,
                     include_rts: Optional[bool] = False,
                     include_replies: Optional[bool] = False,
                     db: Session = Depends(get_db)):
    """`q`で指定される人物のツイートを最大`maxResults`個返します。
    公式マークがついている場合のみツイートを返し、それ以外は`null`を返します。"""
    res = Twitter_Search_Instance(read_twitter_auth_first(db))\
          .twitter_user_search(q, maxResults, include_rts, include_replies)
    return res, 200


#その人のAPIキー一覧
@router.get("/get_twitter_auth_list/")
def get_twitter_auth_list(whose: str, db: Session = Depends(get_db)):
    res = read_twitter_auth_list(db, whose)
    return res, 200

# APIキーを登録
@router.post("/register_twitter_key/")
async def register_twitter_key(data: TwitterSchema,  db: Session = Depends(get_db)):
    req = TwitterModel(whose=data.whose, nankome=data.nankome, api_key=data.api_key, api_key_secret=data.api_key_secret, 
                access_token=data.access_token, access_token_secret=data.access_token_secret)
    db.add(req)
    db.commit()
    res = read_twitter_row(db, data.whose, data.nankome)
    return res, 201

# APIキーを更新
@router.put("/update_twitter_key/")
async def update_twitter_key(data: TwitterSchema, db: Session = Depends(get_db)):
    req = read_twitter_row(db, data.whose, data.nankome)
    req.api_key = data.api_key
    req.api_key_secret = data.api_key_secret
    req.access_token = data.access_token
    req.access_token_secret = data.access_token_secret
    db.commit()
    return None, 204

# APIキーを削除
@router.delete("/delete_twitter_key/")
async def delete_twitter_key(whose: str, nankome: int, db: Session = Depends(get_db)):
    req = read_twitter_row(db, whose, nankome)
    db.delete(req)
    db.commit()
    return None, 204
