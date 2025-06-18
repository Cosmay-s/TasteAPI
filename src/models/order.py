from sqlalchemy import String, Enum, DateTime, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from typing import List
from src.models.dish import Base, Dish
from datetime import datetime

order_dish = Table(
    "order_dish",
    Base.metadata,
    mapped_column("order_id", ForeignKey("orders.id")),
    mapped_column("dish_id", ForeignKey("dishes.id"))
)

class OrderStatus(PyEnum):
    IN_PROCESSING = "в обработке"
    PREPARING = "готовится"
    DELIVERING = "доставляется"
    COMPLETED = "завершен"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String, nullable=False)
    order_time: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.IN_PROCESSING)
    dishes: Mapped[List["Dish"]] = relationship(secondary=order_dish)