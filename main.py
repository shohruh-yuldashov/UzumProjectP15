from fastapi import APIRouter, FastAPI

from auth.auth import register_router

app = FastAPI(title='Uzum', version='1.0.0')

router = APIRouter()

app.include_router(router, prefix='/main')
app.include_router(register_router)
