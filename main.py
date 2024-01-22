from fastapi import APIRouter, FastAPI

app = FastAPI(title='Uzum', version='1.0.0')

router = APIRouter()

app.include_router(router, prefix='main/')
