import jwt
from fastapi.requests import Request
from fastapi import HTTPException

from auth.utils import decode_jwt


def get_user_id(request: Request):
    headers = request.headers
    try:
        token = headers["Authorization"].replace("Bearer ", "")
    except (KeyError, AttributeError):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")
    try:
        content = decode_jwt(token)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Expired token")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token")

    return content["user_id"]
