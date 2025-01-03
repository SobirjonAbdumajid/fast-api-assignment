from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Float, DateTime, Text
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    category = Column()


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, unique=True)
    customer_id = Column(Integer, ForeignKey('users.id'))
    order_date = Column(DateTime, default=datetime.utcnow())
    status = Column()
    total_amount = Column(Float)


class OrderDetails(Base):
    __tablename__ = 'order_details'

    id = Column(Integer, primary_key=True, unique=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    unit_price = Column(Float)




