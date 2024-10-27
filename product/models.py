from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DECIMAL

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String, nullable=True)
    price = Column(DECIMAL)
    quantity = Column(Integer)
    is_available = Column(Boolean, default=True)
    shop_id = Column(Integer, ForeignKey("shops.id"))