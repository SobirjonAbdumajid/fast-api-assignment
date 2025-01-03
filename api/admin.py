from http.client import HTTPException

from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import ProductBase
from models import Product

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/add")
async def add_product(db: db_dependency, product: ProductBase):
    product = db_dependency(product)
    if not product:
        raise HTTPException()

