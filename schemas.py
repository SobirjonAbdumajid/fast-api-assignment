from datetime import datetime, timezone

from pydantic import BaseModel, Field



class UserBase(BaseModel):
    email: str
    full_name: str


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str


class OrderBase(BaseModel):
    order_date: datetime
    status: str
    total_amount: float


# id = Column(Integer, primary_key=True)
#     customer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
#     status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
#     total_amount = Column(Float, nullable=False)