from datetime import datetime
from pydantic import BaseModel


class Like(BaseModel):
    product_id : int

class Comment(BaseModel):
    product_id:int
    comment:str


class Liked_products(BaseModel):
    product_id : int
    created_at:datetime