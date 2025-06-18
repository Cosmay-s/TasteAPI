from fastapi import Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.repositories.order import OrderRepository
from src.schemas.order import OrderCreate, OrderResponse

class OrderService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = OrderRepository(db)

    def get_orders(self) -> list[OrderResponse]:
        return self.repo.get_all()

    def create_order(self, order: OrderCreate) -> OrderResponse:
        return self.repo.create(order)

    def cancel_order(self, order_id: int) -> OrderResponse:
        return self.repo.cancel(order_id)

    def update_status(self, order_id: int, status: str) -> OrderResponse:
        return self.repo.update_status(order_id, status)