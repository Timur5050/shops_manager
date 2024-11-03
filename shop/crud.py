import simplejson as json
from typing import List, Type, Any

from sqlalchemy.orm import Session

from product.models import Product
from settings import settings
from shop.models import Shop

from shop.schemas import ShopCreateSchema


def create_shop(shop: ShopCreateSchema, user_id: int, db: Session) -> Shop:
    shop_obj = Shop(
        title=shop.title,
        description=shop.description,
        phone=shop.phone,
        user_id=user_id
    )
    db.add(shop_obj)
    db.commit()
    db.refresh(shop_obj)
    if shop.products:
        for product in shop.products:
            product_obj = Product(
                title=product.title,
                description=product.description,
                price=product.price,
                quantity=product.quantity,
                is_available=product.is_available,
                shop_id=shop_obj.id
            )
            db.add(product_obj)
            db.commit()
            db.refresh(product_obj)

    redis_client = settings.redis.get_redis_client()
    for key in redis_client.scan_iter("shop*"):
        redis_client.delete(key)

    return shop_obj


def get_all_shops(db: Session) -> list[Shop] | list[Type[Shop]]:
    cache_key = "shops"
    cache_value = settings.redis.get_redis_client().get(cache_key)
    if cache_value:
        print("here")
        shops = [Shop(**shop) for shop in json.loads(cache_value)]
        return shops

    shops = db.query(Shop).all()

    temp_shops = json.dumps([shop.to_dict() for shop in shops])
    settings.redis.get_redis_client().set(cache_key, temp_shops, ex=3600)

    return shops


def get_current_user_shop_list(db: Session, user_id: int) -> list[Shop] | Any:
    cache_key = f"shop_user{user_id}"
    cache_value = settings.redis.get_redis_client().get(cache_key)
    if cache_value:
        shops = [Shop(**shop) for shop in json.loads(cache_value)]
        return shops

    shops_queryset = db.query(Shop).filter(Shop.user_id == user_id)
    temp_shops = json.dumps([shop.to_dict() for shop in shops_queryset])
    settings.redis.get_redis_client().set(cache_key, temp_shops, ex=3600)

    return shops_queryset


def get_details_of_shop(db: Session, shop_id: int):
    cache_key = f"shop{shop_id}"
    cache_value = settings.redis.get_redis_client().get(cache_key)

    if cache_value:
        shop = json.loads(cache_value)
        products = shop.pop("products")
        result_shop = Shop(**shop)
        result_shop.products = products

        return result_shop

    shop_from_db = db.query(Shop).filter(Shop.id == shop_id).first()
    products_to_shop = db.query(Product).filter(Product.shop_id == shop_from_db.id)
    shop_from_db.products = products_to_shop

    temp_shop = shop_from_db.to_dict()
    temp_shop.update({
        "products": [product.to_dict() for product in products_to_shop]
    })

    temp_shop = json.dumps(temp_shop)
    settings.redis.get_redis_client().set(cache_key, temp_shop, ex=3600)

    return shop_from_db
