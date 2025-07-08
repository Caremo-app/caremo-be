from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..repositories.persona_repositories import PersonaRepository
from ..repositories.emailfamily_repositories import EmailFamilyRepository
from ..models.persona_models import PersonaEntity
from ..schemas.persona_schema import PersonaCreateSchema, PersonaReadSchema

class PersonaController:
    def __init__(self, db: Session):
        self.db = db
        self.persona_repo = PersonaRepository(db)
        self.email_repo = EmailFamilyRepository(db)

    def create_persona(self, persona_data: PersonaCreateSchema) -> PersonaReadSchema:
        # Validate that email exists
        email_owner = self.email_repo.get_by_email(persona_data.email)
        if not email_owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email not registered in email_family_entity."
            )

        # Check if this persona (email + name) already exists
        existing_result = self.persona_repo.get_persona_by_email_and_name(
            persona_data.email,
            persona_data.name
        )
        existing = existing_result.scalar_one_or_none()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Persona '{persona_data.name}' already exists for this email."
            )

        new_persona = PersonaEntity(
            email=persona_data.email,
            name=persona_data.name,
            phone_number=persona_data.phone_number,
            role=persona_data.role
        )
        created = self.persona_repo.create_persona(new_persona)
        return PersonaReadSchema.from_orm(created)
    
    def get_persona_by_email(self, email: str) -> PersonaReadSchema:
        result = self.persona_repo.get_persona_by_email(email)
        persona = result.scalar_one_or_none() if result else None

        if not persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona not found."
            )
        return PersonaReadSchema.from_orm(persona)
