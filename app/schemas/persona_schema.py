# schemas/persona_schema.py
from pydantic import BaseModel, EmailStr
from enum import Enum

class RoleEnum(str, Enum):
    RELAY = "relay"
    RECEIVER = "receiver"

class PersonaCreateSchema(BaseModel):
    email: str #EmailStr
    phone_number: str
    name: str
    role: RoleEnum

class PersonaReadSchema(PersonaCreateSchema):
    id: int
    
    class Config:
        from_attributes = True
