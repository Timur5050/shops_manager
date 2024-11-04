import asyncio
import time

import simplejson as json

from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from product.models import Product
from product.schemas import ProductCreateSeparatelySchema, ProductCreateWithShopSchema, ProductsListCreateSchema
from settings import settings


def create_product(product: ProductCreateSeparatelySchema, db: Session) -> Product:
    product_obj = Product(
        title=product.title,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        is_available=product.is_available,
        shop_id=product.shop_id
    )

    db.add(product_obj)
    db.commit()
    db.refresh(product_obj)

    redis_client = settings.redis.get_redis_client()
    for key in redis_client.scan_iter("product*"):
        redis_client.delete(key)

    redis_client.delete(f"shop{product.shop_id}")

    return product_obj


def delete_product(product_id: int, db: Session):
    product_to_delete = db.query(Product).filter(Product.id == product_id).first()
    shop_id_of_deleted_product = product_to_delete.shop_id
    db.delete(product_to_delete)
    db.commit()
    redis_client = settings.redis.get_redis_client()
    for key in redis_client.scan_iter("product*"):
        redis_client.delete(key)

    redis_client.delete(f"shop{shop_id_of_deleted_product}")


async def create_many_products(
        products: list[ProductCreateWithShopSchema],
        shop_id: int,
        db: AsyncSession
):
    products_to_db = [Product(
        title=product.title,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
        is_available=product.is_available,
        shop_id=shop_id
    ) for product in products
    ]
    #await asyncio.sleep(10)
    redis_client = settings.redis.get_redis_client()
    for key in redis_client.scan_iter("product*"):
        redis_client.delete(key)

    redis_client.delete(f"shop{shop_id}")

    async with db.begin():
        db.add_all(products_to_db)
    await db.commit()


def get_products_by_shop(
        shop_id: int,
        db: Session,
        available: bool | None
) -> list[Product]:
    start_time = time.time()
    cache_key = f"products{shop_id}"
    cache_value = settings.redis.get_redis_client().get(cache_key)
    if cache_value:
        products = [Product(**product) for product in json.loads(cache_value)]
       # print("redis:", time.time() - start_time)
        return products

    start_time = time.time()
    product_queryset = db.query(Product).filter(Product.shop_id == shop_id)
    if available is not None:
        product_queryset = product_queryset.filter(Product.is_available == available)
    product_queryset = product_queryset.all()

    temp = json.dumps([product.to_dict() for product in product_queryset])
    settings.redis.get_redis_client().set(cache_key, temp, ex=3600)

   # print("db: ", time.time() - start_time)
    return product_queryset


def retrieve_product_by_id(
        shop_id: int,
        product_id: int,
        db: Session
) -> Product:
    return db.query(Product).filter(
        Product.shop_id == shop_id,
        Product.id == product_id
    ).first()
