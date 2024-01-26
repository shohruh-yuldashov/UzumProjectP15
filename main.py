from fastapi import APIRouter, FastAPI
# from product.product import product_details

from typing import List

from fastapi import APIRouter, FastAPI, Depends
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import verify_token
from database import get_async_session
from scheme import LocationScheme, CityScheme, CityGETScheme, LocationPostScheme

from models.models import locations, city, regions

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.params import Depends
from fastapi.security import oauth2, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.utils import verify_token
from database import get_async_session
from schemes import *
from sqlalchemy import insert

from models.models import *

from auth.auth import register_router
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(title='Uzum', version='1.0.0')

router = APIRouter()


app.include_router(router, prefix='/main')
app.include_router(register_router)

# app.include_router(product_details)


@app.get('/locations')
async def get_locations(
        session: AsyncSession = Depends(get_async_session)
):
    query = select(locations)
    location__data = await session.execute(query)
    location_data = location__data.all()

    lis = []
    for i in location_data:
        print(i)
        query_c = select(city).where(city.c.id == i[4])
        cities = await session.execute(query_c)
        city_data = cities.first()
        dic = {
            'id': i[0],
            'name': i[1],
            'city': {
                'id': city_data[0],
                'name': city_data[1]
            },
            'longitude': i[2],
            'latitude': i[3],
            'opens_at': i[5],
            'closes_at': i[6],
            'has_dressing_room': i[4]
        }
        lis.append(dic)

    await session.commit()

    return lis


@app.post('/locations-add')
async def add_location(
        location_data: LocationPostScheme,
        session=Depends(get_async_session),
        token: dict = Depends(verify_token)
):

    query = insert(locations).values(
        name=location_data.name,
        city_id=location_data.city,
        latitude=location_data.latitude,
        longitude=location_data.longitude,
        opens_at=location_data.opens_at,
        closes_at=location_data.closes_at,
        has_dressing_room=location_data.has_dressing_room
    )
    await session.execute(query)
    await session.commit()
    return {'success': True}


@app.get('/location/{id}')
async def get_city(
        city_id: int,
        session=Depends(get_async_session)
):
    query = select(locations).where(locations.c.city_id == city_id)
    location__data = await session.execute(query)
    location_data = location__data.all()
    lis = []
    for loc in location_data:
        dic = {
            'id': loc.id,
            'name': loc.name,
            'longitude': loc.longitude,
            'latitude': loc.latitude,
            'opens_at': loc.opens_at,
            'closes_at': loc.closes_at,
            'has_dressing_room': loc.has_dressing_room
        }
        lis.append(dic)
    await session.commit()
    return lis


@app.get('/city/{id}', response_model=List[CityGETScheme])
async def get_city(
        region_id: int,
        session=Depends(get_async_session)
):
    query = select(city).where(city.c.region_id == region_id)
    city__data = await session.execute(query)
    city_data = city__data.all()
    await session.commit()
    return city_data


User = users


@router.post('/add-cart')
async def add_cart(
        cart_data: CartItem,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    if token is None:
        raise HTTPException(status_code=403, detail='Forbidden')
    userid = token.get('user_id')

    query1 = select(shopping_cart).where(
        (shopping_cart.c.user_id == userid) & (shopping_cart.c.product_id == cart_data.product_id))
    cart__data = await session.execute(query1)
    cartdata = cart__data.fetchall()
    for item in cartdata:
        if item[2] == userid and item[1] == cart_data.product_id:
            return {'success': False, "message": 'Cart already added'}

    query = insert(shopping_cart).values(**dict(cart_data), user_id=userid)
    await session.execute(query)
    await session.commit()
    return {'success': True}


@router.get('/cart')
async def get_cart(
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    if token is None:
        raise HTTPException(status_code=403, detail='Forbidden')
    userid = token.get('user_id')

    query = select(shopping_cart).where(shopping_cart.c.user_id == userid)
    cart_data = await session.execute(query)
    cart_items = cart_data.fetchall()

    if not cart_items:
        return {'success': True, 'message': 'Cart is empty', 'cart': []}

    cart = []
    for item in cart_items:
        cart.append({
            'product_id': item.product_id,
            'quantity': item.count,
        })

    return {'success': True, 'cart': cart}


@router.delete('/delete_cart')
async def delete_cart_item(
        product_id: int,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    if token is None:
        raise HTTPException(status_code=403, detail='Forbidden')
    userid = token.get('user_id')

    query = select(shopping_cart).where(
        (shopping_cart.c.user_id == userid) & (shopping_cart.c.product_id == product_id)
    )
    cart_data = await session.execute(query)
    cart_item = cart_data.fetchone()

    if cart_item is None:
        raise HTTPException(status_code=404, detail='Item not found in the cart')

    query_delete = delete(shopping_cart).where(
        (shopping_cart.c.user_id == userid) & (shopping_cart.c.product_id == product_id)
    )
    await session.execute(query_delete)
    await session.commit()

    return {'success': True, 'message': 'Item removed from the cart'}


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
app.include_router(register_router, prefix='/auth')
