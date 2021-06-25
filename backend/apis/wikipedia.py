from typing import Optional
from fastapi import APIRouter, Query
from apis.api_components.wikipedia_fetch import wikipedia_fetch_prof

router = APIRouter()


@router.get("/get_wikipedia_prof/")
def get_wikipedia_prof(q: str, count: Optional[int] = Query(None, ge=1)):
    try:
        prof = wikipedia_fetch_prof(q)
    except Exception as e:
        # Wikipedia にページ/Infobox がない場合？
        return None, 404

    if count:
        # python>=3.7
        prof = dict(list(prof.items())[:count])

    return prof, 200
