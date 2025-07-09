from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..db.database import Base
from .vitaldata_models import VitalData
import enum

class RoleEnum(str, enum.Enum):
    RELAY = "relay"
    RECEIVER = "receiver"

class PersonaEntity(Base):
    __tablename__ = "persona_entity"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, ForeignKey("email_family_entity.email"), nullable=False)
    name = Column(String)
    role = Column(Enum(RoleEnum), nullable=False)
    phone_number = Column(String, nullable=False)

    email_family = relationship("EmailFamilyEntity", back_populates="personas")
    vital_data = relationship("VitalData", back_populates="persona", cascade="all, delete-orphan")
