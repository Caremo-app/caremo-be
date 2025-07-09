from fastapi import HTTPException
from ..repositories.emailfamily_repositories import EmailFamilyRepository
from ..util.hash_encryption import hash_password, verify_password
from ..models.emailfamily_models import EmailFamilyEntity  # Assuming you have this
from typing import List

class EmailFamilyController:
    def __init__(self, repo: EmailFamilyRepository):
        self.repo = repo

    def create_user(self, email: str, password: str) -> EmailFamilyEntity:
        existing = self.repo.get_by_email(email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = hash_password(password)
        return self.repo.create(email, hashed_password)

    def sign_in(self, email: str, password: str) -> EmailFamilyEntity:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return user

    def get_user(self, email: str) -> EmailFamilyEntity:
        user = self.repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_family_personas(self, email: str) -> List:
        user = self.repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Defensive: ensure user has attribute `personas`
        if not hasattr(user, 'personas'):
            raise HTTPException(status_code=500, detail="User has no persona relation")

        return user.personas
