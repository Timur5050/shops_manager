from fastapi import APIRouter, Depends
from fastapi.requests import Request
from sqlalchemy.orm import Session
from fastapi import HTTPException

from dependencies import get_db
from shop.models import Shop
from shop.schemas import ShopCreateSchema, ShopRetrieveSchema, ShopDetailSchema
from auth.middleware import get_user_id
from shop import crud

router = APIRouter(prefix="/shop", tags=["shop"])


@router.post("/", response_model=ShopRetrieveSchema)
def create_shop(request: Request, shop: ShopCreateSchema, db: Session = Depends(get_db)):
    user_id = get_user_id(request)

    if db.query(Shop).filter(Shop.title == shop.title).first():
        raise HTTPException(status_code=400, detail="this title is already taken")

    return crud.create_shop(
        shop=shop,
        user_id=user_id,
        db=db
    )


@router.get("/shops/", response_model=list[ShopRetrieveSchema])
def get_all_shops(request: Request, my: bool = False, db: Session = Depends(get_db)):
    if my:
        user_id = get_user_id(request)
        return crud.get_current_user_shop_list(
            db=db,
            user_id=user_id
        )
    return crud.get_all_shops(
        db=db
    )


@router.get("/shops/{shop_id}/", response_model=ShopDetailSchema)
def get_details_of_shop(request: Request, shop_id: int, db: Session = Depends(get_db)):
    get_user_id(request)

    return crud.get_details_of_shop(
        db=db,
        shop_id=shop_id
    )
