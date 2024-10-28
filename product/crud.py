import asyncio

from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from product.models import Product
from product.schemas import ProductCreateSeparatelySchema, ProductCreateWithShopSchema, ProductsListCreateSchema


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
    # await asyncio.sleep(10)
    async with db.begin():
        db.add_all(products_to_db)
    await db.commit()


