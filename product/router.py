from urllib.parse import unquote

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from sqlalchemy.orm import Session

from auth.middleware import get_user_id
from dependencies import get_db
from product.models import Product
from product.schemas import ProductCreateSeparatelySchema, ProductRetrieveSchema
from product import crud
from shop.models import Shop

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductRetrieveSchema)
def create_product(
        request: Request,
        product: ProductCreateSeparatelySchema,
        db: Session = Depends(get_db)
):
    user_id = get_user_id(request)

    shop_from_db = db.query(Shop).filter(Shop.id == product.shop_id).first()

    if not shop_from_db or shop_from_db.user_id != user_id:
        raise HTTPException(status_code=400, detail="invalid shop id")

    return crud.create_product(
        product=product,
        db=db
    )


@router.delete("/{shop_id}/{product_id}/")
def delete_product(
        request: Request,
        product_id: int,
        shop_id: id,
        db: Session = Depends(get_db)
):
    user_id = get_user_id(request)

    shop_from_db = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop_from_db or shop_from_db.user_id != user_id:
        raise HTTPException(status_code=400, detail="no such shop connected to you")

    product_from_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_from_db or product_from_db.shop_id != shop_from_db.id:
        raise HTTPException(status_code=400, detail="no such product in such shop")

    crud.delete_product(product_id=product_id, db=db)
