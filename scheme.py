from datetime import datetime, date, time
from sqlalchemy import Date
from pydantic import BaseModel


class RegionsScheme(BaseModel):
    id: int
    name: str


class CityGETScheme(BaseModel):
    id: int
    name: str


class CityScheme(BaseModel):
    id: int
    name: str
    region: RegionsScheme


class LocationScheme(BaseModel):
    id: int
    name: str
    city: CityScheme
    longitude: float
    latitude: float


class LocationPostScheme(BaseModel):
    name: str
    city: int
    longitude: float
    latitude: float
    opens_at: time
    closes_at: time
    has_dressing_room: bool


class ProductCreate(BaseModel):
    name: str
    count: int
    price: float
    colour: str
    description: str


class ProductInfo(BaseModel):
    name: str
    count: int
    price: float
    colour: str
    description: str

