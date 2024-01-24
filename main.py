from typing import List

from fastapi import APIRouter, FastAPI, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import verify_token
from database import get_async_session
from scheme import LocationScheme, CityScheme

from models.models import locations, city, regions

from auth.auth import register_router

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
        query_c = select(city).where(city.c.id==i[2])
        cities = await session.execute(query_c)
        city_data = cities.first()
        query_r = select(regions).where(regions.c.id == i[3])
        regions__data = await session.execute(query_r)
        regions_data = regions__data.first()
        print(city_data)
        dic = {
            'id': i[0],
            'name': i[1],
            'city': {
                'id': city_data[0],
                'name': city_data[1]
            },
            'regions': {
                'id': regions_data[0],
                'name': regions_data[1]
            },
        }
        lis.append(dic)

    await session.commit()

    return lis


@app.post('/locations-add')
async def add_location(
        location_data: LocationScheme,
        session=Depends(get_async_session),
):

    query = insert(locations).values(
        name=location_data.name,
        city_id=location_data.city.id,
        region_id=location_data.regions.id
    )
    await session.execute(query)
    await session.commit()
    return {'success': True}

