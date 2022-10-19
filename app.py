from fastapi import FastAPI, APIRouter
from routers import user_routers


app = FastAPI()
router = APIRouter()

@router.get('/')
def hello_world():
    return "Hello world"

app.include_router(router)
app.include_router(user_routers)