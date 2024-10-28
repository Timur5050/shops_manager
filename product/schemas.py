import decimal

from pydantic import BaseModel


class ProductCreateWithShopSchema(BaseModel):
    title: str
    description: str | None = None
    price: decimal.Decimal
    quantity: int
    is_available: bool | None = None


class ProductCreateSeparatelySchema(ProductCreateWithShopSchema):
    shop_id: int


class ProductRetrieveSchema(BaseModel):
    id: int
    title: str
    description: str
    price: decimal.Decimal
    quantity: int
    is_available: bool
    shop_id: int


class ProductsListCreateSchema(BaseModel):
    products: list[ProductCreateWithShopSchema]
