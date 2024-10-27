from pydantic import BaseModel, field_validator

from product.schemas import ProductCreateWithShopSchema


class ShopCreateSchema(BaseModel):
    title: str
    description: str
    phone: str
    products: list[ProductCreateWithShopSchema] | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone: str):
        if len(phone) != 13 or phone[:4] != "+380" or not phone[4:].isnumeric():
            raise ValueError("Phone number must start with +380 and contain 9 digits after the country code.")
        return phone


class ShopRetrieveSchema(BaseModel):
    id: int
    title: str
    description: str
    phone: str
    user_id: int
