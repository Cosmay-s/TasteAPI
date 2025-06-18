from fastapi import Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.repositories.dish import DishRepository
from src.schemas.dish import DishCreate, DishResponse

class DishService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = DishRepository(db)

    def get_dishes(self) -> list[DishResponse]:
        return self.repo.get_all()

    def create_dish(self, dish: DishCreate) -> DishResponse:
        return self.repo.create(dish)

    def delete_dish(self, dish_id: int) -> DishResponse:
        return self.repo.delete(dish_id)