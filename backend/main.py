from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from apis.oshido import router as oshido_router
from apis.recommend import router as recommend_router
from apis.youtube import router as youtube_router
from apis.twitter import router as twitter_router
from apis.news import router as news_router
from apis.wikipedia import router as wp_router
from apis.combined import router as combined_router

router = APIRouter()
router.include_router(
    oshido_router,
)
router.include_router(
    recommend_router,
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
router.include_router(
    wp_router,
)
router.include_router(
    combined_router,
)
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)