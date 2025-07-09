# models/emailfamily_models.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from ..db.database import Base

class EmailFamilyEntity(Base):
    __tablename__ = "email_family_entity"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    personas = relationship("PersonaEntity", back_populates="email_family", cascade="all, delete-orphan")