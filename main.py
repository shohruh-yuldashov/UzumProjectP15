
from typing import List

from fastapi import APIRouter, FastAPI, Depends
from sqlalchemy import select, insert
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
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(title='Uzum', version='1.0.0')

router = APIRouter()



app.include_router(router, prefix='/main')
app.include_router(register_router)


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
        query_c = select(city).where(city.c.id==i[4])
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



app.include_router(router, prefix='/main')
app.include_router(register_router, prefix='/auth')

