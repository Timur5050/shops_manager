from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks
from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from auth.middleware import get_user_id
from database import AsyncSessionLocal
from dependencies import get_db, get_async_db
from product.models import Product
from product.schemas import ProductCreateSeparatelySchema, ProductRetrieveSchema, ProductCreateWithShopSchema, \
    ProductsListCreateSchema, ProductListSchema
from product import crud
from shop.models import Shop

router = APIRouter(prefix="/products", tags=["products"])


def check_unique_of_products(
        shop_id: int,
        products: ProductsListCreateSchema | ProductCreateSeparatelySchema,
        db: Session
):
    products_for_db = [product.title for product in db.query(Product).filter(Product.shop_id == shop_id)]

    if isinstance(products, ProductsListCreateSchema):
        duplicates = []
        for product in products.products:
            if product.title in products_for_db:
                duplicates.append(product.title)
        if duplicates:
            raise HTTPException(
                status_code=400,
                detail=f"his shop already has products with name(s): {", ".join(duplicates)}"
            )
    else:
        if products.title in products_for_db:
            raise HTTPException(
                status_code=400,
                detail=f"this shop already has products with name: {products.title}"
            )


@router.post("/", response_model=ProductRetrieveSchema)
def create_product(
        request: Request,
        product: ProductCreateSeparatelySchema,
        db: Session = Depends(get_db)
):
    user_id = get_user_id(request)

    shop_from_db = db.query(Shop).filter(Shop.id == product.shop_id).first()

    check_unique_of_products(
        shop_id=product.shop_id,
        products=product,
        db=db
    )

    if not shop_from_db or shop_from_db.user_id != user_id:
        raise HTTPException(status_code=400, detail="invalid shop id")

    return crud.create_product(
        product=product,
        db=db
    )


@router.delete("/{shop_id}/{product_id}/", response_model=None)
def delete_product(
        request: Request,
        product_id: int,
        shop_id: int,
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


@router.post("/add/{shop_id}/", response_model=None)
async def create_many_products(
        request: Request,
        shop_id: int,
        products: ProductsListCreateSchema,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
):
    user_id = get_user_id(request)

    shop_from_db = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop_from_db or shop_from_db.user_id != user_id:
        raise HTTPException(status_code=400, detail="no such shop connected to you")

    check_unique_of_products(
        shop_id=shop_id,
        products=products,
        db=db
    )

    async with AsyncSessionLocal() as async_db:
        background_tasks.add_task(
            crud.create_many_products,
            products=products.products,
            shop_id=shop_id,
            db=async_db
        )

    return JSONResponse(
        {"message": "Products are being added successfully!"}
    )


@router.get("/{shop_id}/", response_model=list[ProductListSchema])
def get_products_from_shop(
        request: Request,
        shop_id: int,
        db: Session = Depends(get_db),
        available: bool | None = None
):
    get_user_id(request)

    return crud.get_products_by_shop(
        shop_id=shop_id,
        db=db,
        available=available
    )


@router.get("/{shop_id}/{product_id}/", response_model=ProductRetrieveSchema)
def retrieve_product_by_id(
        request: Request,
        shop_id: int,
        product_id: int,
        db: Session = Depends(get_db)
):
    get_user_id(request)

    return crud.retrieve_product_by_id(
        shop_id=shop_id,
        product_id=product_id,
        db=db
    )
