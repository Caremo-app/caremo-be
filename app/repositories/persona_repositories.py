from sqlalchemy.orm import Session
from sqlalchemy.future import select
from ..models.persona_models import PersonaEntity

class PersonaRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_persona_by_email(self, email: str):
        result = self.db.execute(
            select(PersonaEntity).where(PersonaEntity.email == email)
        )
        return result
    
    def get_persona_by_email_and_name(self, email: str, name: str):
        return self.db.execute(
            select(PersonaEntity).where(
                PersonaEntity.email == email,
                PersonaEntity.name == name
            )
        )
    
    def create_persona(self, persona: PersonaEntity) -> PersonaEntity:
        self.db.add(persona)
        self.db.commit()
        self.db.refresh(persona)
        return persona
    
    def update_persona(self, persona: PersonaEntity) -> PersonaEntity:
        self.db.commit()
        self.db.refresh(persona)
        return persona
    
    def delete_persona(self, persona: PersonaEntity) -> None:
        self.db.delete(persona)
        self.db.commit()