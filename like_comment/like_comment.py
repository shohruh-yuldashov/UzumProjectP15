import secrets
import random
import json

from sqlalchemy.ext.asyncio import AsyncSession

from models.models import like, comment
from datetime import datetime, timedelta
from like_comment.schema import Like,Comment
from auth.utils import generate_token, verify_token, send_email_report_dashboard
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import get_async_session
from sqlalchemy import select, insert

@app.post("/like")
def like_product(like: Like,token : dict = Depends(verify_token), session: AsyncSession = Depends(get_async_session)):



@app.post("/comment")
def write_comment(comment: Comment):
    #
    #
    return {"success": True, "message": "Comment posted successfully!"}

