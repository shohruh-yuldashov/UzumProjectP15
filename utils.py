import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import SMTP_USER, SMTP_PASSWORD
from database import get_async_session
from models.models import users


async def get_user_email(user_id, session: AsyncSession = Depends(get_async_session)):
    select_user_query = select(users).where(users.c.id == user_id)
    user__data = await session.execute(select_user_query)
    user_data = user__data.fetchone()
    return user_data[3]


async def send_email_notification(user_email: str, subject: str, message: str):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_username = SMTP_USER
    smtp_password = SMTP_PASSWORD

    sender_email = SMTP_USER
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, user_email, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")
