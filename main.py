from fastapi import FastAPI
from api import customer, admin

app = FastAPI()

app.include_router(customer.router)
app.include_router(admin.router)

