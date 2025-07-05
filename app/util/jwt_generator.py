from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from jwt import decode, encode, ExpiredSignatureError, PyJWTError
import os

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET")

bearer_scheme = HTTPBearer(auto_error=False)

def create_access_token(user_email: str):
    payload = {
        "sub": user_email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        "iat": datetime.now(timezone.utc),
        "type": "access"
    }
    return encode(payload, JWT_SECRET, algorithm="HS256")

def create_refresh_token(user_email: str):
    payload = {
        "sub": user_email,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "iat": datetime.now(timezone.utc),
        "type": "refresh"
    }
    return encode(payload, JWT_REFRESH_SECRET, algorithm="HS256")

def decode_refresh_token(token: str):
    try:
        payload = decode(token, JWT_REFRESH_SECRET, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

def verify_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = credentials.credentials
    try:
        payload = decode(token, JWT_SECRET, algorithms=["HS256"])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
