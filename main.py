from fastapi import APIRouter, FastAPI
import secrets
from auth.auth import register_router
from like_comment.like_comment import like_comment

app = FastAPI(title='Uzum', version='1.0.0')

router = APIRouter()

app.include_router(router, prefix='/main')
app.include_router(register_router)
app.include_router(like_comment)
