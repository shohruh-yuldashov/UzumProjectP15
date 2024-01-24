import datetime

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
    opens_at: datetime.time
    closes_at: datetime.time
    has_dressing_room: bool

