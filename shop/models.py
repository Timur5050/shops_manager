from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base


class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    description = Column(String, nullable=True)
    phone = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
