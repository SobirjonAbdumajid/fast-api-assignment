from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Order, User
from auth import get_current_user
from schemas import OrderBase

from models import Product

router = APIRouter(
    prefix="/api",
    tags=["customer"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# @router.get("/products")
# async def get_products(user: user_dependency, db: db_dependency):
#     products = db.query(Product).filter(User.id == user.get('id')).all()
#     return products

@router.get("/products")
async def get_products(db: db_dependency):
    products = db.query(Product).all()
    return products

@router.post('/order')
async def create_order(
    user: user_dependency,
    db: db_dependency,
    new_order: OrderBase
):
    if not user.get("id"):
        raise HTTPException(status_code=400, detail="User ID is required")

    order_model = Order(customer_id=user["id"], **new_order.dict())
    db.add(order_model)
    db.commit()
    db.refresh(order_model)
    return order_model


@router.get('/order/{order_id}/status')
async def get_order_status(order_id: str, db: db_dependency, user: user_dependency):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": order.id, "status": order.status}

@router.get('/orders')
async def get_orders(db: db_dependency, user: user_dependency):
    orders = db.query(Order).filter(Order.customer_id == user.get('id')).all()
    return orders
