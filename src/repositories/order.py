from sqlalchemy.orm import Session
from src.models.order import Order, OrderStatus
from src.models.dish import Dish
from src.schemas.order import OrderCreate
from fastapi import HTTPException


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Order).all()

    def create(self, order: OrderCreate):
        dishes = self.db.query(Dish).filter(Dish.id.in_(order.dish_ids)).all()
        if len(dishes) != len(order.dish_ids):
            raise HTTPException(status_code=400, detail="Некоторые блюда не найдены")
        
        db_order = Order(customer_name=order.customer_name)
        db_order.dishes = dishes
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def cancel(self, order_id: int):
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")
        if order.status != OrderStatus.IN_PROCESSING:
            raise HTTPException(status_code=400, detail="Заказ можно отменить только в статусе 'в обработке'")
        self.db.delete(order)
        self.db.commit()
        return order

    def update_status(self, order_id: int, new_status: str):
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")
        
        status_order = [OrderStatus.IN_PROCESSING, OrderStatus.PREPARING, OrderStatus.DELIVERING, OrderStatus.COMPLETED]
        try:
            new_status_enum = OrderStatus(new_status)
        except ValueError:
            raise HTTPException(status_code=400, detail="Недопустимый статус")
        
        current_idx = status_order.index(order.status)
        new_idx = status_order.index(new_status_enum)
        
        if new_idx != current_idx + 1:
            raise HTTPException(status_code=400, detail="Недопустимый переход статуса")
        
        order.status = new_status_enum
        self.db.commit()
        self.db.refresh(order)
        return order