from sqlalchemy.orm import Session
from src.models.dish import Dish
from src.schemas.dish import DishCreate

class DishRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Dish).all()

    def create(self, dish: DishCreate):
        db_dish = Dish(**dish.dict())
        self.db.add(db_dish)
        self.db.commit()
        self.db.refresh(db_dish)
        return db_dish

    def delete(self, dish_id: int):
        dish = self.db.query(Dish).filter(Dish.id == dish_id).first()
        if dish:
            self.db.delete(dish)
            self.db.commit()
        return dish