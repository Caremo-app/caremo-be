from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from ...controllers.user_controllers import get_users_controller
from ...oauth import oauth
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
async def google_auth_callback(request: Request):
    print(request.url)
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.get("userinfo", token=token)
        user_info = user_info.json()
        
        return JSONResponse({
            "access_token": token["access_token"],
            "user": user_info
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google OAuth failed: {e}")