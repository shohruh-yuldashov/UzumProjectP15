from pydantic import BaseModel


class CityScheme(BaseModel):
    id: int
    name: str


class RegionsScheme(BaseModel):
    id: int
    name: str


class LocationScheme(BaseModel):
    name: str
    city: CityScheme
    regions: RegionsScheme

