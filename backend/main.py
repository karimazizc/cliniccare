"""FastAPI main application for ClinicCare Mini EMR."""

from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import engine, get_db, Base
from models import DiagnosisCode, Consultation
from schemas import (
    DiagnosisCodeResponse,
    ConsultationCreate,
    ConsultationResponse,
    ConsultationListResponse,
    ErrorResponse
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="ClinicCare Mini EMR",
    description="A lightweight Electronic Medical Records system for clinic consultations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ClinicCare Mini EMR API",
        "version": "1.0.0"
    }


@app.get(
    "/api/diagnosis",
    response_model=List[DiagnosisCodeResponse],
    tags=["Diagnosis Codes"],
    summary="Search ICD-10 diagnosis codes",
    responses={
        200: {"description": "List of matching diagnosis codes"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def search_diagnosis_codes(
    search: Optional[str] = Query(None, description="Search term for code or description"),
    db: Session = Depends(get_db)
):
    """
    Search ICD-10 diagnosis codes by code or description.
    
    - **search**: Optional search term (case-insensitive partial match)
    - Returns maximum 20 results for performance
    """
    try:
        query = db.query(DiagnosisCode)
        
        if search and search.strip():
            search_term = f"%{search.strip().lower()}%"
            query = query.filter(
                or_(
                    DiagnosisCode.code.ilike(search_term),
                    DiagnosisCode.description.ilike(search_term)
                )
            )
        
        # Limit results for performance
        codes = query.order_by(DiagnosisCode.code).limit(20).all()
        return codes
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching diagnosis codes: {str(e)}"
        )


@app.post(
    "/api/consultation",
    response_model=ConsultationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Consultations"],
    summary="Create a new consultation",
    responses={
        201: {"description": "Consultation created successfully"},
        400: {"model": ErrorResponse, "description": "Bad request"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def create_consultation(
    consultation: ConsultationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new patient consultation.
    
    - **patient_name**: Patient's full name (required)
    - **diagnosis_codes**: List of ICD-10 codes (required, at least one)
    - **treatment_notes**: Treatment notes and recommendations (required)
    - **consultation_date**: Optional date of consultation (defaults to current time)
    """
    try:
        # Validate diagnosis codes exist in database
        for code in consultation.diagnosis_codes:
            existing_code = db.query(DiagnosisCode).filter(
                DiagnosisCode.code == code
            ).first()
            if not existing_code:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid diagnosis code: {code}"
                )
        
        # Create consultation
        db_consultation = Consultation(
            patient_name=consultation.patient_name,
            diagnosis_codes=consultation.diagnosis_codes,
            treatment_notes=consultation.treatment_notes,
            consultation_date=consultation.consultation_date or datetime.utcnow(),
            created_at=datetime.utcnow()
        )
        
        db.add(db_consultation)
        db.commit()
        db.refresh(db_consultation)
        
        return db_consultation
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating consultation: {str(e)}"
        )


@app.get(
    "/api/consultations",
    response_model=ConsultationListResponse,
    tags=["Consultations"],
    summary="List all consultations",
    responses={
        200: {"description": "List of consultations"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def list_consultations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    List all patient consultations ordered by date descending.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    try:
        total = db.query(Consultation).count()
        consultations = (
            db.query(Consultation)
            .order_by(Consultation.consultation_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return ConsultationListResponse(
            consultations=consultations,
            total=total
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching consultations: {str(e)}"
        )


@app.get(
    "/api/consultation/{consultation_id}",
    response_model=ConsultationResponse,
    tags=["Consultations"],
    summary="Get consultation by ID",
    responses={
        200: {"description": "Consultation details"},
        404: {"model": ErrorResponse, "description": "Consultation not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_consultation(
    consultation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific consultation by ID.
    
    - **consultation_id**: The unique identifier of the consultation
    """
    try:
        consultation = db.query(Consultation).filter(
            Consultation.id == consultation_id
        ).first()
        
        if not consultation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Consultation with ID {consultation_id} not found"
            )
        
        return consultation
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching consultation: {str(e)}"
        )


@app.delete(
    "/api/consultation/{consultation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Consultations"],
    summary="Delete consultation",
    responses={
        204: {"description": "Consultation deleted successfully"},
        404: {"model": ErrorResponse, "description": "Consultation not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def delete_consultation(
    consultation_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a consultation by ID.
    
    - **consultation_id**: The unique identifier of the consultation to delete
    """
    try:
        consultation = db.query(Consultation).filter(
            Consultation.id == consultation_id
        ).first()
        
        if not consultation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Consultation with ID {consultation_id} not found"
            )
        
        db.delete(consultation)
        db.commit()
        
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting consultation: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
