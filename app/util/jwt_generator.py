import jwt
from datetime import datetime, timedelta
import os

from fastapi import Depends, HTTPException, Header

SECRET = os.environ.get("JWT_SECRET")

def create_jwt(user_email: str):
    payload = {
        "sub": user_email,
        "exp": datetime.now(datetime.timezone.now) + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")