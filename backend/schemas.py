"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator


# Diagnosis Code Schemas
class DiagnosisCodeBase(BaseModel):
    """Base schema for diagnosis code."""
    code: str
    description: str


class DiagnosisCodeResponse(DiagnosisCodeBase):
    """Response schema for diagnosis code."""
    id: int
    
    class Config:
        from_attributes = True


# Consultation Schemas
class ConsultationCreate(BaseModel):
    """Schema for creating a consultation."""
    patient_name: str = Field(..., min_length=1, max_length=255, description="Patient's full name")
    diagnosis_codes: List[str] = Field(..., min_items=1, description="List of ICD-10 diagnosis codes")
    treatment_notes: str = Field(..., min_length=1, description="Treatment notes and recommendations")
    consultation_date: Optional[datetime] = Field(None, description="Date of consultation")
    
    @validator('patient_name')
    def validate_patient_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Patient name is required')
        return v.strip()
    
    @validator('treatment_notes')
    def validate_treatment_notes(cls, v):
        if not v or not v.strip():
            raise ValueError('Treatment notes are required')
        return v.strip()
    
    @validator('diagnosis_codes')
    def validate_diagnosis_codes(cls, v):
        if not v:
            raise ValueError('At least one diagnosis code is required')
        return [code.strip() for code in v if code.strip()]


class ConsultationResponse(BaseModel):
    """Response schema for consultation."""
    id: int
    patient_name: str
    diagnosis_codes: List[str]
    treatment_notes: str
    consultation_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConsultationListResponse(BaseModel):
    """Response schema for consultation list."""
    consultations: List[ConsultationResponse]
    total: int


# Error Schemas
class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str


class ValidationErrorResponse(BaseModel):
    """Schema for validation error responses."""
    detail: List[dict]
