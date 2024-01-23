import smtplib
import secrets
import jwt
from email.message import EmailMessage

from datetime import datetime, timedelta
from config import SECRET
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from celery import Celery

from config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')


algorithm = 'HS256'
security = HTTPBearer()


def generate_token(user_id: int):
    jti_access = secrets.token_urlsafe(32)
    jti_refresh = secrets.token_urlsafe(32)

    payload_access = {
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(minutes=30),
        'user_id': user_id,
        'jti': jti_access
    }
    payload_refresh = {
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(days=1),
        'user_id': user_id,
        'jti': jti_refresh
    }
    access_token = jwt.encode(payload_access, SECRET, algorithm=algorithm)
    refresh_token = jwt.encode(payload_refresh, SECRET, algorithm=algorithm)
    return {
        'access': access_token,
        'refresh': refresh_token
    }


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token is expired!')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Token invalid!')


def get_email_template_dashboard(user_email, code):
    email = EmailMessage()
    email['Subject'] = f'Verify email'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        f"""
        <div>
            <h1 style="color: black;"> Hi!😊 </h1>
            <h1 style="color: black;"> Thank you for joining Uzum </h1>
            <h1 style="color: black;">Enter the verification code below to activate your account: </h1>
            <h1 style="margin: 0; padding-right: 2px; width: 90px ; background-color: green; color: white;"> {code} </h1>
        </div>
        """,
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(email: str, code: int):
    email = get_email_template_dashboard(email, code)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
