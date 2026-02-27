import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, cast
from fastapi import Depends, HTTPException, status


pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

authDeps = Annotated[str, Depends(oauth2_scheme)]

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

"""
    Auth Settings Here
"""

SECRET_KEY = "janedoe123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRED_IN_MINUTES = 1

def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRED_IN_MINUTES)
    payload.update({ "exp": expire })
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return cast(dict, token)