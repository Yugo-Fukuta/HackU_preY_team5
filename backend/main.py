from fastapi import FastAPI, APIRouter
from apis.oshido import router as oshido_router

router = APIRouter()
router.include_router(
    oshido_router,
)

app = FastAPI()
app.include_router(router)