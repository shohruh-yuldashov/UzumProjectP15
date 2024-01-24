from pydantic import BaseModel

class Like(BaseModel):
    product_id: int


class Comment(BaseModel):
    product_id: int
    comment: str
