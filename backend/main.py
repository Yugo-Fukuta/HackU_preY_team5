from fastapi import FastAPI, APIRouter
from apis.oshido import router as oshido_router
from apis.youtube import router as youtube_router

router = APIRouter()
router.include_router(
    oshido_router,
)
router.include_router(
    youtube_router,
)
app = FastAPI()
app.include_router(router)