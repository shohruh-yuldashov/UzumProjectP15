from celery.schedules import crontab
from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.models import user_payment, PaymentEnum, credit, credit_choice

from celery import shared_task, Celery

from utils import get_user_email, send_email_notification

celery = Celery(
    "tasks",
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

celery.conf.beat_schedule = {
    'process-monthly-payments': {
        'task': 'tasks.process_monthly_payments',
        'schedule': crontab(day_of_month='1'),
    },
}


@shared_task
async def process_monthly_payments(session: AsyncSession = Depends(get_async_session)):
    payments_query = select(user_payment).where(
        (user_payment.c.status == PaymentEnum.active) &
        (user_payment.c.payed_month < user_payment.c.payment_for_month)
    )
    payments = await session.execute(payments_query)

    for payment in payments.fetchall():
        user_id = payment[1]
        payed_month = payment[5] + 1
        payed_amount = payment[3] / payment[2]
        new_payed_amount = payment[4] + payed_amount
        update_payment_query = (
            update(user_payment)
            .where(user_payment.c.user_id == user_id)
            .values(
                payed_month=payed_month,
                payed_amount=new_payed_amount
            )
        )
        await session.execute(update_payment_query)
        select_credit_query = select(credit).where(credit.c.id == payment[6])
        credit__data = await session.execute(select_credit_query)
        credit_data = credit__data.fetchone()
        select_choice_query = select(credit_choice).where(credit_choice.c.id == credit_data[3])
        choice__data = await session.execute(select_choice_query)
        choice_data = choice__data.fetchone()
        if choice_data[1] == payment[2]:
            update_payment_status_query = (
                update(user_payment)
                .where(user_payment.c.user_id == user_id)
                .values(status=PaymentEnum.payed)
            )
            await session.execute(update_payment_status_query)
            return {"success": True, "detail": "The users payed for product successfully"}
        user_email = await get_user_email(user_id)
        html_content = ("""
            <html>
            <head></head>
            <body>
                <h2>Hello,</h2>
                <p>This is a notification that your payment has been processed.</p>
                <p>Thank you for your payment!</p>
            </body>
            </html>
            """)
        await send_email_notification(user_email, "Pay your payment", html_content)

# for work this celery you can use this code
# celery -A tasks beat --loglevel=info
