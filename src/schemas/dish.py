from pydantic import BaseModel
from typing import Optional

class DishBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    category: str

class DishCreate(DishBase):
    pass

class DishResponse(DishBase):
    id: int

    class Config:
        orm_mode = True