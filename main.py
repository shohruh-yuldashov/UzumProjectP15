from fastapi import APIRouter, FastAPI
from product.product import product_details
from auth.auth import register_router

app = FastAPI(title='Uzum', version='1.0.0')

router = APIRouter()

app.include_router(router, prefix='/main')
app.include_router(register_router)
app.include_router(product_details)
