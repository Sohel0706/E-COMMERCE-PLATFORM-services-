from pydantic import BaseModel
from pydantic import Field


class CartItemCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True
