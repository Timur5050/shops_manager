from typing import List, Type

from sqlalchemy.orm import Session

from product.models import Product
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

    return shop_obj


def get_all_shops(db: Session) -> list[Type[Shop]]:
    return db.query(Shop).all()


def get_current_user_shop_list(db: Session, user_id: int) -> list[Type[Shop]]:
    return db.query(Shop).filter(Shop.user_id == user_id)


def get_details_of_shop(db: Session, shop_id: int):
    shop_from_db = db.query(Shop).filter(Shop.id == shop_id).first()
    products_to_shop = db.query(Product).filter(Product.shop_id == shop_from_db.id)
    shop_from_db.products = products_to_shop
    return shop_from_db
