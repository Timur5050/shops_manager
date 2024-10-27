from fastapi import FastAPI

from user import router as user_router
from shop import router as shop_router
from product import router as product_router

app = FastAPI()

app.include_router(user_router.router)
app.include_router(shop_router.router)
app.include_router(product_router.router)
