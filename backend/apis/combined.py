from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session, sessionmaker
from database import get_db, SessionLocal
from apis.youtube import get_youtube_data
from apis.twitter import get_twitter_data
from apis.news import get_news_data
from apis.wikipedia import get_wikipedia_prof
import random
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()

# YouTubeからデータ取得
@router.get("/get_combined_data/")
def get_combined_data(q: str, maxResults: int, db: Session = Depends(get_db)):
    '''
    res_yt = get_youtube_data(q, maxResults, db)[0]
    res_tw = get_twitter_data(q, maxResults, db)[0]
    res_nw = get_news_data(q, db)[0]
    res_wk = get_wikipedia_prof(q, maxResults)[0]
    return res_yt, res_tw, res_nw, res_wk
    '''
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        res_yt = executor.submit(get_youtube_data, q, maxResults, db)
        res_tw = executor.submit(get_twitter_data, q, maxResults, db)
        res_nw = executor.submit(get_news_data, q, db)
        res_wk = executor.submit(get_wikipedia_prof, q, maxResults)
    return res_yt.result()[0], res_tw.result()[0], res_nw.result()[0], res_wk.result()[0]