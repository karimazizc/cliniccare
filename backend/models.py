"""SQLAlchemy ORM models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON

from database import Base


class DiagnosisCode(Base):
    """ICD-10 Diagnosis Code model."""
    
    __tablename__ = "diagnosis_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)


class Consultation(Base):
    """Patient Consultation model."""
    
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(255), nullable=False, index=True)
    diagnosis_codes = Column(JSON, nullable=False, default=list)
    treatment_notes = Column(Text, nullable=False)
    consultation_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
