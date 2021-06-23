from fastapi import FastAPI, APIRouter
from apis.oshido import router as oshido_router
from apis.youtube import router as youtube_router
from apis.twitter import router as twitter_router
from apis.news import router as news_router

router = APIRouter()
router.include_router(
    oshido_router,
)
router.include_router(
    youtube_router,
)
router.include_router(
    twitter_router,
)
router.include_router(
    news_router,
)
app = FastAPI()
app.include_router(router)
