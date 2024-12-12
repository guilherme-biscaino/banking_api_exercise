import time
from typing import Annotated
from fastapi.security.http import HTTPAuthorizationCredentials
from typing_extensions import Annotated, Doc
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

SECRET = "secret_made_key"
ALGORITHM = "HS256"


class AccessToken(BaseModel):
    iss: str
    sub: int
    aud: str
    exp: float
    iat: float
    ngf: float
    jti: str


class JWTToken(BaseModel):
    access_token: AccessToken


def sign_jwt(user_id: int) -> JWTToken:
    now = time.time()

    payload = {
        "iss": "curso_fast_api",   
        "sub": user_id,
        "aud": "curso_fast_api",
        "exp": now + (60 * 30),
        "iat": now,
        "ngf": now,
        "jti": uuid4().hex,
    }

    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {"access_token": token}


async def decode_jwt(token: str) -> JWTToken | None:
    try:
        decoded_token = jwt.decode(token, SECRET, audience="curso_fast_api", options={"verify_sub": False, "verify_jti": False}, algorithms=[ALGORITHM])
        _token = JWTToken.model_validate({"access_token": decoded_token})

        return _token if _token.access_token.exp >= time.time() else None
    except Exception as test:
        return None

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> JWTToken:
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if credentials:
            if not scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="1")
            payload = await decode_jwt(credentials)
            if not payload:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="2")
            return payload
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="3")


async def get_current_user(token: Annotated[JWTToken, Depends(JWTBearer())]) -> dict[str, int]:
    return {"user_id": token.access_token.sub}


def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return current_user