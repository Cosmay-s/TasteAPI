from pydantic import BaseModel
from datetime import datetime
from typing import List
from src.schemas.dish import DishResponse

class OrderBase(BaseModel):
    customer_name: str
    dish_ids: List[int]

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    order_time: datetime
    status: str
    dishes: List[DishResponse]

    class Config:
        orm_mode = True