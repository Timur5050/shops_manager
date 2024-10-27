import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from dependencies import get_db
from user.schemas import UserRetrieveSchema, UserSchema
from user.models import User
from auth.utils import get_password_hash, verify_password, encode_jwt, decode_jwt
from user import crud

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register/", response_model=UserRetrieveSchema)
def register_user(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    password = get_password_hash(user.password)
    user.password = password

    return crud.create_user(
        db=db,
        user=user,
    )


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return False
    if not verify_password(password, db_user.password):
        return False
    return db_user


@router.post("/login/")
def login_user(user: UserSchema, db: Session = Depends(get_db)):
    user_in_db = authenticate_user(user.email, user.password, db)
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Email or password incorrect")

    general_payload = {
        "email": user_in_db.email,
        "user_id": user_in_db.id,
    }

    access_payload = general_payload.copy()
    access_payload["token_type"] = "access"

    refresh_payload = general_payload.copy()
    refresh_payload["token_type"] = "refresh"

    access_token = encode_jwt(payload=access_payload)
    refresh_token = encode_jwt(payload=refresh_payload)

    response_content = {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    response = JSONResponse(response_content)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True
    )

    return response


@router.post("/token/refresh/")
async def refresh_old_token(request: Request):
    body = await request.json()
    refresh_token = body.get("refresh_token")
    try:
        payload = decode_jwt(refresh_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")

    new_payload = {
        "email": payload.get("email"),
        "user_id": payload.get("user_id"),
        "token_type": "access"
    }
    new_access_token = encode_jwt(payload=new_payload)
    response_content = {"access_token": new_access_token}

    response = JSONResponse(response_content)
    response.set_cookie(key="access_token", value=new_access_token, httponly=True, secure=True)

    return response
