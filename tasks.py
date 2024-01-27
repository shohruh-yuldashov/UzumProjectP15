from fastapi import Depends
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from celery import Celery

from database import get_async_session
from models.models import promocodes, PromoEnum

celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


@celery.task(serializer='json')
async def check_promo_time(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(promocodes).where(
            promocodes.c.date <= datetime.utcnow,
            promocodes.c.status == PromoEnum.active
        )
        promo_result = await session.execute(query)
        result = promo_result.all()

        for item in result:
            promo_id = item[0]
            update_query = update(promocodes).where(promo_id == promocodes.c.id).values(status=PromoEnum.expires)
            await session.execute(update_query)
        await session.commit()

    except Exception as e:
        print(e)
