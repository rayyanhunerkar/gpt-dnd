import time
from typing import Any

import jwt
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from starlette.requests import Request

from ..configs.settings import JWTSettings


def token_response(access_token: str, user: dict) -> dict:
    return {
        "access_token": access_token,
        "id": user["id"],
        "email": user["email"],
        "createdAt": user["created_at"],
        "updatedAt": user["updated_at"]
    }


def create_access_token(user: dict) -> str:
    payload = {
        "id": str(user["id"]),
        "email": user["email"],
        "name": user['name'],
        "expires": time.time() + 5260000
    }
    access_token = jwt.encode(payload, JWTSettings.secret_key, algorithm=JWTSettings.algo)
    return access_token


def sign_jwt(user: dict) -> dict[str, Any]:
    access_token = create_access_token(user)
    return token_response(access_token, user)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWTSettings.secret_key, algorithms=[JWTSettings.algo])
        return decoded_token
    except Exception:
        raise


def verify_jwt(token: str) -> bool:
    is_token_valid: bool = False

    try:
        payload = decode_jwt(token)
    except Exception:
        payload = None
        raise
    if payload:
        is_token_valid = True
    return is_token_valid


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
