from sqlalchemy.orm import Session, selectinload
from ..models.emailfamily_models import EmailFamilyEntity

class EmailFamilyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(EmailFamilyEntity).options(
            selectinload(EmailFamilyEntity.personas)
        ).filter(EmailFamilyEntity.email == email).first()
    
    def create(self, email: str, hashed_password: str):
        new_user = EmailFamilyEntity(email=email, password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
