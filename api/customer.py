from fastapi import APIRouter, Depends
from database import SessionLocal, engine
from typing import Annotated
from sqlalchemy.orm import Session
from schemas import ProductBase

from models import Product

router = APIRouter(
    prefix="/api",
    tags=["api"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/products")
async def get_products(db: db_dependency):
    return db.query(Product).all()
