from datetime import datetime, date

from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.utils import verify_token
from database import get_async_session
from models.models import credit, products, user_payment, credit_choice

from auth.auth import register_router

app = FastAPI(title='Uzum', version='1.0.0')

router = APIRouter()


@router.post('/credit_product')
async def credit_product(
        product_id: int,
        choice_id: int,
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
            choice=choice_id
        )
        await session.execute(insert_query)
        await session.commit()
        return {"detail": "Product successfully added to cart with credit", "status": status.HTTP_201_CREATED}
    except IntegrityError:
        raise HTTPException(detail='This product is already in the cart', status_code=status.HTTP_204_NO_CONTENT)
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
        data = {}
        for i, j in enumerate(product_data):
            body = {
                'id': j[0],
                'user_id': j[1],
                'product_id': j[2],
                'choice': j[3],
                'created_at': j[4]
            }
            data.update({f"{i + 1}-data": body})
        print(data)
        return {"product_data": data}
    except Exception as e:
        raise HTTPException(detail=f'{e}', status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/pay-product{product_id}')
async def pay_product(
        product_id: int,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    if token is None:
        raise HTTPException(detail='Token not provided!!!', status_code=status.HTTP_401_UNAUTHORIZED)
    user_id = token.get('user_id')
    existing_credit_product_query = select(credit).where(credit.c.product_id == product_id)
    result = await session.execute(existing_credit_product_query)
    if result.scalars().one() is None:
        raise HTTPException(detail='This product is not found in your credit cart',
                            status_code=status.HTTP_404_NOT_FOUND)
    try:
        result_data = result.fetchone()
        credit_id = result_data[0]
        select_credit_query = select(credit).where(credit.c.id == credit_id)
        credit__data = await session.execute(select_credit_query)
        credit_data = credit__data.fetchone()
        choice_id = credit_data[0]
        select_choice_query = select(credit_choice).where(credit_choice.c.id == choice_id)
        choice__data = await session.execute(select_choice_query)
        choice_data = choice__data.fetchone()
        select_product_query = select(products.c.price).where(products.c.id == product_id)
        price__data = await session.execute(select_product_query)
        price_data = price__data.fetchone()
        new_price_data = price_data[0] + (price_data[0] / 100 * 30)
        payment_for_month = new_price_data / int(choice_data[1])

        insert_query = insert(user_payment).values(
            user_id=user_id,
            payment_for_month=payment_for_month,
            payment_price=new_price_data,
            payed_amout=0,
            payed_month=0,
            credit_id=credit_id
        )
        await session.execute(insert_query)
        await session.commit()

    except Exception as e:
        raise HTTPException(detail=f'{e}', status_code=status.HTTP_400_BAD_REQUEST)


app.include_router(router, prefix='/main')
app.include_router(register_router)
