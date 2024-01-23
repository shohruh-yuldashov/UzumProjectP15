import redis
import secrets
import random
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from models.models import users
from datetime import datetime, timedelta
from auth.schema import UserRegister, User_In_Db, User_Info
from auth.utils import generate_token, verify_token, send_email_report_dashboard
from database import get_async_session
from sqlalchemy import select, insert

register_router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


@register_router.post('/register')
async def register(
        user_data: UserRegister,
        session: AsyncSession = Depends(get_async_session)
):
    if user_data.password1 == user_data.password2:
        user_exists = await session.execute(select(users).where(users.c.username == user_data.username))
        user_exists_value = user_exists.scalar()

        if user_exists_value is not None:
            return {'success': False, 'message': 'Username already exists!'}

        email_exists = await session.execute(select(users).where(users.c.email == user_data.email))
        email_exists_value = email_exists.scalar()

        if email_exists_value is not None:
            return {'success': False, 'message': 'Email already exists!'}

        hash_password = pwd_context.hash(user_data.password1)
        user_in_db = User_In_Db(**dict(user_data), password=hash_password, balance=1000000)
        query = insert(users).values(**dict(user_in_db))
        await session.execute(query)
        await session.commit()
        user_info = User_Info(**dict(user_in_db))
        return dict(user_info)
    else:
        raise HTTPException(status_code=400, detail='Passwords are not the same !')


@register_router.get('/login')
async def login(
        email: str
):
    if not select(users).where(users.c.email == email).exists:
        raise HTTPException(status_code=400, detail='Email not found!!!')

    token = secrets.token_urlsafe(32)

    code = random.randint(99999, 999999)

    redis_client.set(f'{token}', json.dumps({'code': code, 'email': email}), ex=600)


    send_email_report_dashboard(email, code)

    return {'token': token, 'message': 'Please verify your email'}


@register_router.get('/verify-email')
async def verify_email(
        token: str,
        code: int,
        session: AsyncSession = Depends(get_async_session)
):

    data = redis_client.get(f'{token}')
    if data is None:
        raise HTTPException(status_code=404, detail='Token not found !!!')

    data = json.loads(data)

    if data['code'] == code:
        query = select(users).where(users.c.email == data['email'])
        user_data = await session.execute(query)

        try:
            user_data = user_data.one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail='User not found !')

        token = generate_token(user_data.id)

        redis_client.delete(f'{token}')

        return token

    else:
        raise HTTPException(status_code=401, detail='Code is invalid !')


@register_router.get('/user-info', response_model=User_Info)
async def user_info(token: dict = Depends(verify_token), session: AsyncSession = Depends(get_async_session)):
    if token is None:
        raise HTTPException(status_code=401, detail='No Registered !')
    user_id = token.get('user_id')
    query = select(users).where(users.c.id == user_id)
    user_data = await session.execute(query)
    try:
        user_data = user_data.one()
        return User_Info(**user_data._asdict())
    except NoResultFound:
        raise HTTPException(status_code=404, detail='User not found !')
