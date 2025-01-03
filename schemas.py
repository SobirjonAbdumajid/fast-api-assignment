from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    full_name: str


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str


    # id = Column(Integer, primary_key=True)
    # name = Column(String)
    # description = Column(String)
    # price = Column(Float)
    # stock = Column(Integer)
    # category = Column(Enum(Category))