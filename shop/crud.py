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
