from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import ProductBase
from models import Product, Order
from auth import get_current_user

router = APIRouter(
    prefix="/api",
    tags=["admin"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/products")
async def add_product(user: user_dependency, db: db_dependency, product: ProductBase):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed - admin can")
    try:
        product_model = Product(**product.dict())
        db.add(product_model)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/products/{product_id}")
async def get_product(user: user_dependency, db: db_dependency, product_id: int):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=400, detail="Authentication Failed - admin can")
    the_product = db.query(Product).filter(Product.id == product_id).first()
    return the_product


@router.put("/products/{product_id}")
async def update_product(user: user_dependency, db: db_dependency, product_request: ProductBase, product_id: int):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=400, detail="Authentication Failed - admin can")
    product_model = db.query(Product).filter(Product.id == product_id).first()
    if product_model is None:
        raise HTTPException(status_code=404, detail="Product not found")

    product_model.name = product_request.name
    product_model.description = product_request.description
    product_model.price = product_request.price
    product_model.stock = product_request.stock
    product_model.category = product_request.category

    db.add(product_model)
    db.commit()


@router.delete("/products/{product_id}")
async def delete_product(user: user_dependency, db: db_dependency, product_id: int):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=400, detail="Authentication Failed - admin can")
    product_model = db.query(Product).filter(Product.id == product_id).first()
    if product_model is None:
        raise HTTPException(status_code=400, detail="Product not found")
    db.delete(product_model)
    db.commit()


@router.get('/orders/{order_id}')
async def get_order(user: user_dependency, db: db_dependency, order_id: int):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=404, detail="Authentication Failed - admin can")

    order = db.query(Order).filter(Order.id == order_id).first()

    return order



@router.get('/all-orders')
async def get_all_orders(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=400, detail="Authentication Failed - admin can")

    return db.query(Order).all()