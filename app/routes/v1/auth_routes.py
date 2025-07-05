from fastapi import APIRouter, Request, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from ...oauth import oauth
from sqlalchemy.orm import Session
from ...repositories.emailfamily_repositories import EmailFamilyRepository
from ...controllers.emailfamily_controllers import EmailFamilyController
from ...util.jwt_generator import create_access_token, create_refresh_token
from ...repositories.refreshtoken_repositories import RefreshTokenRepository
from ...controllers.refreshtoken_controllers import RefreshTokenController
from ...util.use_db import get_db

import os

router = APIRouter(
    prefix="/v1/auth",
    tags=["Auth"]
)

@router.get("/google")
async def get_users(request: Request):
    print(request.url)
    redirect_uri = os.environ.get("GOOGLE_AUTH_CALLBACK_URI").strip()
    print("Redirect URI:", redirect_uri)
    print("Redirect URI repr:", repr(redirect_uri))
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.get("userinfo", token=token)
        user_info = user_info.json()

        email = user_info.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email not found from Google")

        # Try to find or create user
        repo = EmailFamilyRepository(db)
        controller = EmailFamilyController(repo)
        user = controller.get_user(email)

        if not user:
            # If user does not exist, register a dummy password
            user = controller.create_user(email=email, password="GOOGLE_OAUTH_DEFAULT")

        jwt_token = create_access_token(email)
        refresh_token = create_refresh_token(email)

        return {
            "access_token": jwt_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "email": user.email
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google OAuth failed: {e}")
    
@router.post("/signup")
async def emailfamily_signup(email: str, password: str, db: Session = Depends(get_db)):
    try:
        
        repo = EmailFamilyRepository(db)
        controller = EmailFamilyController(repo)
        controller.create_user(email, password)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User created successfully"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/signin")
async def emailfamily_signin(email: str, password: str, db: Session = Depends(get_db)):
    try:
        repo = EmailFamilyRepository(db)
        controller = EmailFamilyController(repo)
        user = controller.sign_in(email, password)
        
        jwt_token = create_access_token(email)
        refresh_token = create_refresh_token(email)
        
        return {
            "access_token": jwt_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "email": user.email
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    repo = RefreshTokenRepository(db)
    controller = RefreshTokenController(repo)
    return controller.rotate_token(refresh_token)

@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    repo = RefreshTokenRepository(db)
    controller = RefreshTokenController(repo)
    return controller.logout(refresh_token)