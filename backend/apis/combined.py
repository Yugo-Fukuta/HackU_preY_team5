from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session, sessionmaker
from database import get_db, SessionLocal
from apis.youtube import get_youtube_data
from apis.twitter import get_twitter_data
from apis.news import get_news_data
from apis.wikipedia import get_wikipedia_prof
from models.api_cache import APICacheModel
import random
from concurrent.futures import ThreadPoolExecutor

def read_api_cache_row(db_session: Session, celeb_name: str):
    return db_session.query(APICacheModel).filter(APICacheModel.celeb_name == celeb_name).first()

router = APIRouter()

@router.get("/get_combined_data/")
def get_combined_data(celeb_name: str, maxResults: int, db: Session = Depends(get_db)):
    '''
    res_yt = get_youtube_data(q, maxResults, db)[0]
    res_tw = get_twitter_data(q, maxResults, db)[0]
    res_nw = get_news_data(q, db)[0]
    res_wk = get_wikipedia_prof(q, maxResults)[0]
    return res_yt, res_tw, res_nw, res_wk
    '''
    res_yt = res_tw = res_nw = None
    yt_put = tw_put = nw_put = True
    post_flag = False
    put_flag = False
    com = read_api_cache_row(db, celeb_name)

    if com ==  None:
        post_flag = True
    else:
        if com.yt_cache:
            res_yt = com.yt_cache
            yt_put = False
        if com.tw_cache:
            res_tw = com.tw_cache
            tw_put = False
        if com.nw_cache:
            res_nw = com.nw_cache
            nw_put = False

    if (yt_put or tw_put or nw_put) == True:
        put_flag = True
        with ThreadPoolExecutor(max_workers=3) as executor:
            if res_yt == None:
                res_yt = executor.submit(get_youtube_data, celeb_name, maxResults, db).result()[0]
            if res_tw == None:
                res_tw = executor.submit(get_twitter_data, celeb_name, maxResults, db).result()[0]["statuses"]
            if res_nw == None:
                res_nw = executor.submit(get_news_data, celeb_name, db).result()[0]["articles"]
            #res_wk = executor.submit(get_wikipedia_prof, celeb_name, maxResults)

        #res_yt = yt.result()[0]
        #res_tw = tw.result()[0]["statuses"]
        #res_nw = nw.result()[0]["articles"]

        if post_flag:
            req = APICacheModel(celeb_name = celeb_name, yt_cache=res_yt, tw_cache=res_tw, nw_cache=res_nw)
            db.add(req)
            db.commit()
        elif put_flag:
            req = com
            if yt_put:
                req.yt_cache = res_yt
            if tw_put:
                req.tw_cache = res_tw
            if nw_put:
                req.nw_cache = res_nw
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

    res = random.sample(res, len(res))
    return res