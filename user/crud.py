from sqlalchemy.orm import Session

from user.models import User
from user.schemas import UserSchema


def create_user(db: Session, user: UserSchema) -> User:
    user = User(
        email=user.email,
        password=user.password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
