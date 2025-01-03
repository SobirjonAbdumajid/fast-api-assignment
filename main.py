from fastapi import FastAPI
from api import customer, admin
import auth

app = FastAPI()

app.include_router(customer.router)
app.include_router(admin.router)
app.include_router(auth.router)

