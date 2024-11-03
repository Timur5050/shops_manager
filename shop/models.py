from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base


class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    description = Column(String, nullable=True)
    phone = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "phone": self.phone,
            "user_id": self.user_id
        }
