from typing import Optional
from fastapi import APIRouter, Query
#from apis.api_components.wikipedia_fetch import wikipedia_fetch_prof
import urllib.request as req
import urllib.parse as up
#import lxml.html as lh
import json

router = APIRouter()


@router.get("/get_wikipedia_prof/")
def get_wikipedia_prof(q: str, count: Optional[int] = Query(None, ge=1)):
    """
    try:
        prof = wikipedia_fetch_prof(q)
    except Exception as e:
        # Wikipedia にページ/Infobox がない場合？
        prof = {}

    if count:
        # python>=3.7
        prof = dict(list(prof.items())[:count])
    """
    prof = {}
    try:
        s_url = 'https://ja.wikipedia.org/api/rest_v1/page/summary/' + up.quote(q)
        request = req.Request(url=s_url)
        res = req.urlopen(request, timeout=10).read()
        resd = json.loads(res.decode('utf-8'))
        prof = resd
    except:
        return None, 404

    return prof, 200