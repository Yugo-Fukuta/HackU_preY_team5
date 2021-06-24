from fastapi import Depends, APIRouter
from apis.api_components.wikipedia_fetch import wikipedia_fetch_prof

router = APIRouter()


@router.get("/get_wikipedia_prof/")
def get_wikipedia_prof(q: str):
    try:
        prof = wikipedia_fetch_prof(q)
    except Exception as e:
        # Wikipedia にページ/Infobox がない場合？
        return None, 404

    return prof, 200
