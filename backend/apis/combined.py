from typing import Optional
from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session, sessionmaker
from database import get_db, SessionLocal
from apis.youtube import get_youtube_data, get_youtube_channel_data
from apis.twitter import get_twitter_data
from apis.twitter import get_celeb_tweets
from apis.news import get_news_data
from apis.wikipedia import get_wikipedia_prof
from models.api_cache import APICacheModel
from models.trend import TrendModel
import random
from concurrent.futures import ThreadPoolExecutor
import datetime
import pandas as pd
import pandas.tseries.offsets as offsets

def read_api_cache_row(db_session: Session, celeb_name: str):
    return db_session.query(APICacheModel).filter(APICacheModel.celeb_name == celeb_name).first()

def read_trend_row(db_session: Session, celeb_name: str):
    return db_session.query(TrendModel).filter(TrendModel.celeb_name == celeb_name).first()

router = APIRouter()

@router.get("/get_combined_data/")
def get_combined_data(celeb_name: str, maxResults: int, max_yt: Optional[int] = 50, max_tw: Optional[int] = 100, max_official_tw: Optional[int] = 10, db: Session = Depends(get_db)):
    '''
    `maxResults`: フロント側の取得件数, `max_yt`or`max_tw`: バックエンドでのYouTube/Twitter取得件数
    '''
    res_yt = res_tw = res_nw = []
    res_wk = {}
    yt_put = tw_put = nw_put = wk_put = True
    post_flag = False
    put_flag = False
    com = read_api_cache_row(db, celeb_name)

    if com ==  None:
        post_flag = True
    else:
        cached_time = com.updated_at
        current_time = datetime.datetime.utcnow()+ datetime.timedelta(hours=9)
        if pd.Timestamp(current_time.replace(microsecond = 0)) < cached_time+offsets.Hour(3):
            if com.yt_cache:
                res_yt = com.yt_cache
                yt_put = False
            if com.tw_cache:
                res_tw = com.tw_cache
                tw_put = False
            if com.nw_cache:
                res_nw = com.nw_cache
                nw_put = False
            if com.wk_cache:
                res_wk = com.wk_cache
                wk_put = False

    if (yt_put or tw_put or nw_put or wk_put) == True:
        put_flag = True
        with ThreadPoolExecutor(max_workers=6) as executor:
            if res_yt == []:
                res_yt1 = executor.submit(get_youtube_data, celeb_name, max_yt, db).result()[0]
                res_yt2 = executor.submit(get_youtube_channel_data, celeb_name, max_yt, db).result()[0]["videos"]
            if res_tw == []:
                res_tw1 = executor.submit(get_twitter_data, celeb_name, max_tw, db).result()[0]
                res_tw2 = executor.submit(get_celeb_tweets, celeb_name, max_official_tw, False, False, db).result()[0]
            if res_nw == []:
                res_nw = executor.submit(get_news_data, celeb_name, db).result()[0]["articles"]
            if res_wk == {}:
                res_wk = executor.submit(get_wikipedia_prof, celeb_name, 1).result()[0]
        
        if post_flag:
            res_yt = res_yt1 + res_yt2
            res_tw = res_tw1 + res_tw2
            req = APICacheModel(celeb_name = celeb_name, yt_cache=res_yt, tw_cache=res_tw, nw_cache=res_nw, wk_cache=res_wk)
            db.add(req)
            db.commit()
        elif put_flag:
            req = com
            if yt_put:
                res_yt = res_yt1 + res_yt2
                req.yt_cache = res_yt
            if tw_put:
                res_tw = res_tw1 + res_tw2
                req.tw_cache = res_tw
            if nw_put:
                req.nw_cache = res_nw
            if wk_put:
                req.wk_cache = res_wk
            db.commit()

    ret = read_trend_row(db, celeb_name)
    if ret == None:
        req_t = TrendModel(celeb_name=celeb_name, count=1)
        db.add(req_t)
        db.commit()
    else:
        ret.count = ret.count + 1
        db.commit()

    res = []
    for y in res_yt:
        y['where']='youtube'
        res.append(y)
    for t in res_tw:
        t['where']='twitter'
        res.append(t)
    for n in res_nw:
        n['where']='news'
        res.append(n)
    if res_wk != None and res_wk != {}:
        res_wk['where']='wikipedia'

    res = random.sample(res, len(res))[:maxResults]
    res.append(res_wk)
    return res
