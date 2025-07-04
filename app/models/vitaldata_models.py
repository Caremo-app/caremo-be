from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base

class VitalData(Base):
    __tablename__ = "vital_data"

    id = Column(Integer, primary_key=True, index=True)

    # ForeignKey to PersonaEntity
    persona_id = Column(Integer, ForeignKey("persona_entity.id"), nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Vital metrics from smartwatch (example fields)
    heart_rate = Column(Float, nullable=True)  # bpm
    step_count = Column(Integer, nullable=True)
    temperature = Column(Float, nullable=True)  # Celsius
    blood_oxygen = Column(Float, nullable=True)  # SpO2 percentage

    persona = relationship("PersonaEntity", back_populates="vital_data")
