from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..models.refreshtoken_models import RefreshTokenEntity

class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_token(self, email: str, token: str, expires_in_days: int = 7):
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        refresh_token = RefreshTokenEntity(
            token=token,
            email=email,
            expires_at=expires_at
        )
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def get_token(self, token: str):
        return self.db.query(RefreshTokenEntity).filter_by(token=token).first()

    def delete_token(self, token: str):
        token_obj = self.get_token(token)
        if token_obj:
            self.db.delete(token_obj)
            self.db.commit()

    def delete_all_for_user(self, email: str):
        self.db.query(RefreshTokenEntity).filter_by(email=email).delete()
        self.db.commit()
