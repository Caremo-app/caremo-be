from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Header

import jwt
from jwt import PyJWTError, ExpiredSignatureError
import os

JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_REFRESH_SECRET = os.environ.get("JWT_REFRESH_SECRET")

def create_access_token(user_email: str):
    payload = {
        "sub": user_email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def create_refresh_token(email: str, expires_delta=timedelta(days=7)):
    payload = {
        "sub": email,
        "exp": datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(payload, JWT_REFRESH_SECRET, algorithm="HS256")

def decode_refresh_token(token: str):
    return jwt.decode(token, JWT_REFRESH_SECRET, algorithms=["HS256"])

def verify_token(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload  
    
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")