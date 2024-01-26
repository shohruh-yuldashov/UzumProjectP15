from typing import List

from pydantic import BaseModel


class CartItem(BaseModel):
    product_id: int
    count: int


class Cart(BaseModel):
    user_id: int
    items: List[CartItem] = []
