from fastapi import HTTPException
from ..repositories.emailfamily_repositories import EmailFamilyRepository
from ..util.hash_encryption import hash_password, verify_password

class EmailFamilyController:
    def __init__(self, repo: EmailFamilyRepository):
        self.repo = repo

    def create_user(self, email: str, password: str):
        existing = self.repo.get_by_email(email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = hash_password(password)
        return self.repo.create(email, hashed_password)

    def sign_in(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return user
    
    def get_user(self, email: str):
        user = self.repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    def get_family_personas(self, email: str):
        user = self.get_user(email)
        return user.personas
    
