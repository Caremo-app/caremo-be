from ..repositories.refreshtoken_repositories import RefreshTokenRepository
from ..util.jwt_generator import create_access_token, create_refresh_token, decode_refresh_token
import jwt
from fastapi import HTTPException, Header
from datetime import datetime

class RefreshTokenController:
    def __init__(self, repo: RefreshTokenRepository):
        self.repo = repo

    # def issue_tokens(self, email: str):
    #     access_token = create_access_token(email)
    #     refresh_token = create_refresh_token(email)
    #     self.repo.create_token(email, refresh_token)
    #     return {
    #         "access_token": access_token,
    #         "refresh_token": refresh_token
    #     }

    def rotate_token(self, refresh_token: str):
        try:
            payload = decode_refresh_token(refresh_token)
            email = payload.get("sub")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Step 2: Check if token exists in DB
        stored = self.repo.get_token(refresh_token)
        if not stored:
            raise HTTPException(status_code=401, detail="Refresh token not found")

        # Step 3: Expiry check
        if stored.expires_at < datetime.utcnow():
            self.repo.delete_token(refresh_token)
            raise HTTPException(status_code=401, detail="Refresh token expired")

        # Step 4: Rotate token
        self.repo.delete_token(refresh_token)
        new_refresh_token = create_refresh_token(email)
        self.repo.create_token(email, new_refresh_token)

        access_token = create_access_token(email)
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token
        }

    def logout(self, refresh_token: str):
        self.repo.delete_token(refresh_token)
        return {"message": "Logged out"}

    def logout_all(self, email: str):
        self.repo.delete_all_for_user(email)
        return {"message": "All sessions revoked"}