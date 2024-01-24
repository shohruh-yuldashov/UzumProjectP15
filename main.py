from datetime import datetime, date

from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.utils import verify_token
from database import get_async_session
from models.models import CreditEnum, credit, products

from auth.auth import register_router

app = FastAPI(title='Uzum', version='1.0.0')

router = APIRouter()


@router.post('/credit_product')
async def credit_product(
        product_id: int,
        name: CreditEnum,
        deadline: date,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)

):
    if token is None:
        raise HTTPException(detail='Token not provided!!!', status_code=status.HTTP_401_UNAUTHORIZED)
    user_id = token.get('user_id')
    try:
        existing_product_query = select(products).where(products.c.id == product_id)
        result = await session.execute(existing_product_query)
        if result.scalar() is None:
            raise HTTPException(detail='Product not found!!!', status_code=status.HTTP_404_NOT_FOUND)

        insert_query = insert(credit).values(
            user_id=user_id,
            product_id=product_id,
            name=name,
            deadline=deadline
        )
        await session.execute(insert_query)
        await session.commit()
        return {"detail": "Product successfully added to cart with credit", "status": status.HTTP_201_CREATED}
    except IntegrityError:
        raise HTTPException(detail=f'This product already in cart', status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(detail=f'{e}', status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/get-credit-products')
async def get_credit_products(
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session),
):
    if token is None:
        raise HTTPException(detail='Token not provided!!!', status_code=status.HTTP_401_UNAUTHORIZED)
    user_id = token.get('user_id')
    try:
        user_credit_products = select(credit).where(credit.c.user_id == user_id)
        product__data = await session.execute(user_credit_products)
        product_data = product__data.fetchall()
        return {"product_data": product_data}
    except Exception as e:
        raise HTTPException(detail=f'{e}', status_code=status.HTTP_400_BAD_REQUEST)


app.include_router(router, prefix='/main')
app.include_router(register_router)
