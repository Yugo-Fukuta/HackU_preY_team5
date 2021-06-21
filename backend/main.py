'''from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}'''

from fastapi import FastAPI, APIRouter
from apis.oshido import router as oshido_router

router = APIRouter()
router.include_router(
    oshido_router,
    #prefix='/users',
    #tags=['users']
)

app = FastAPI()
app.include_router(router)