from sqlalchemy.orm import Session

from product.models import Product
from product.schemas import ProductCreateSeparatelySchema


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

    return product_obj


def delete_product(product_id: int, db: Session):
    product_to_delete = db.query(Product).filter(Product.id == product_id).first()
    db.delete(product_to_delete)
    db.commit()
