"""Initialize database with ICD-10 diagnosis codes."""

from database import engine, SessionLocal, Base
from models import DiagnosisCode, Consultation

# 100 Common ICD-10 Diagnosis Codes
ICD10_CODES = [
    # Endocrine, Nutritional, and Metabolic Diseases (E00-E89)
    ("E11.9", "Type 2 diabetes mellitus without complications"),
    ("E11.65", "Type 2 diabetes mellitus with hyperglycemia"),
    ("E11.21", "Type 2 diabetes mellitus with diabetic nephropathy"),
    ("E11.40", "Type 2 diabetes mellitus with diabetic neuropathy, unspecified"),
    ("E10.9", "Type 1 diabetes mellitus without complications"),
    ("E03.9", "Hypothyroidism, unspecified"),
    ("E05.90", "Thyrotoxicosis, unspecified without thyrotoxic crisis"),
    ("E78.5", "Hyperlipidemia, unspecified"),
    ("E78.0", "Pure hypercholesterolemia"),
    ("E66.9", "Obesity, unspecified"),
    ("E55.9", "Vitamin D deficiency, unspecified"),
    ("E87.6", "Hypokalemia"),
    
    # Diseases of the Circulatory System (I00-I99)
    ("I10", "Essential (primary) hypertension"),
    ("I11.9", "Hypertensive heart disease without heart failure"),
    ("I25.10", "Atherosclerotic heart disease of native coronary artery"),
    ("I48.91", "Unspecified atrial fibrillation"),
    ("I48.0", "Paroxysmal atrial fibrillation"),
    ("I50.9", "Heart failure, unspecified"),
    ("I50.22", "Chronic systolic (congestive) heart failure"),
    ("I63.9", "Cerebral infarction, unspecified"),
    ("I73.9", "Peripheral vascular disease, unspecified"),
    ("I87.2", "Venous insufficiency (chronic) (peripheral)"),
    ("I83.90", "Asymptomatic varicose veins of unspecified lower extremity"),
    
    # Diseases of the Respiratory System (J00-J99)
    ("J45.909", "Unspecified asthma, uncomplicated"),
    ("J45.20", "Mild intermittent asthma, uncomplicated"),
    ("J45.30", "Mild persistent asthma, uncomplicated"),
    ("J44.9", "Chronic obstructive pulmonary disease, unspecified"),
    ("J44.1", "Chronic obstructive pulmonary disease with acute exacerbation"),
    ("J06.9", "Acute upper respiratory infection, unspecified"),
    ("J20.9", "Acute bronchitis, unspecified"),
    ("J18.9", "Pneumonia, unspecified organism"),
    ("J30.9", "Allergic rhinitis, unspecified"),
    ("J32.9", "Chronic sinusitis, unspecified"),
    ("J02.9", "Acute pharyngitis, unspecified"),
    ("J03.90", "Acute tonsillitis, unspecified"),
    
    # Diseases of the Digestive System (K00-K95)
    ("K21.0", "Gastro-esophageal reflux disease with esophagitis"),
    ("K21.9", "Gastro-esophageal reflux disease without esophagitis"),
    ("K29.70", "Gastritis, unspecified, without bleeding"),
    ("K30", "Functional dyspepsia"),
    ("K58.9", "Irritable bowel syndrome without diarrhea"),
    ("K59.00", "Constipation, unspecified"),
    ("K76.0", "Fatty (change of) liver, not elsewhere classified"),
    ("K80.20", "Calculus of gallbladder without cholecystitis"),
    ("K85.90", "Acute pancreatitis without necrosis or infection, unspecified"),
    
    # Diseases of the Musculoskeletal System (M00-M99)
    ("M79.3", "Panniculitis, unspecified"),
    ("M54.5", "Low back pain"),
    ("M54.2", "Cervicalgia"),
    ("M25.50", "Pain in unspecified joint"),
    ("M17.9", "Osteoarthritis of knee, unspecified"),
    ("M16.9", "Osteoarthritis of hip, unspecified"),
    ("M19.90", "Unspecified osteoarthritis, unspecified site"),
    ("M10.9", "Gout, unspecified"),
    ("M81.0", "Age-related osteoporosis without current pathological fracture"),
    ("M62.830", "Muscle spasm of back"),
    ("M75.100", "Unspecified rotator cuff tear of unspecified shoulder"),
    ("M79.1", "Myalgia"),
    
    # Mental, Behavioral, and Neurodevelopmental Disorders (F01-F99)
    ("F32.9", "Major depressive disorder, single episode, unspecified"),
    ("F33.0", "Major depressive disorder, recurrent, mild"),
    ("F41.1", "Generalized anxiety disorder"),
    ("F41.9", "Anxiety disorder, unspecified"),
    ("F43.10", "Post-traumatic stress disorder, unspecified"),
    ("F51.01", "Primary insomnia"),
    ("F90.9", "Attention-deficit hyperactivity disorder, unspecified type"),
    
    # Diseases of the Genitourinary System (N00-N99)
    ("N39.0", "Urinary tract infection, site not specified"),
    ("N40.0", "Benign prostatic hyperplasia without lower urinary tract symptoms"),
    ("N18.3", "Chronic kidney disease, stage 3 (moderate)"),
    ("N18.9", "Chronic kidney disease, unspecified"),
    ("N95.1", "Menopausal and female climacteric states"),
    
    # Diseases of the Skin and Subcutaneous Tissue (L00-L99)
    ("L30.9", "Dermatitis, unspecified"),
    ("L20.9", "Atopic dermatitis, unspecified"),
    ("L50.9", "Urticaria, unspecified"),
    ("L40.9", "Psoriasis, unspecified"),
    ("L70.0", "Acne vulgaris"),
    ("L03.90", "Cellulitis, unspecified"),
    
    # Diseases of the Eye and Adnexa (H00-H59)
    ("H10.9", "Unspecified conjunctivitis"),
    ("H52.4", "Presbyopia"),
    ("H40.9", "Unspecified glaucoma"),
    ("H26.9", "Unspecified cataract"),
    
    # Diseases of the Ear and Mastoid Process (H60-H95)
    ("H66.90", "Otitis media, unspecified, unspecified ear"),
    ("H61.20", "Impacted cerumen, unspecified ear"),
    
    # Diseases of the Nervous System (G00-G99)
    ("G43.909", "Migraine, unspecified, not intractable, without status migrainosus"),
    ("G47.00", "Insomnia, unspecified"),
    ("G47.33", "Obstructive sleep apnea (adult) (pediatric)"),
    ("G89.29", "Other chronic pain"),
    ("G62.9", "Polyneuropathy, unspecified"),
    
    # Symptoms, Signs, and Abnormal Clinical Findings (R00-R99)
    ("R51.9", "Headache, unspecified"),
    ("R10.9", "Unspecified abdominal pain"),
    ("R05.9", "Cough, unspecified"),
    ("R50.9", "Fever, unspecified"),
    ("R53.83", "Other fatigue"),
    ("R42", "Dizziness and giddiness"),
    ("R00.0", "Tachycardia, unspecified"),
    ("R11.10", "Vomiting, unspecified"),
    ("R63.4", "Abnormal weight loss"),
    
    # Injury, Poisoning, and External Causes (S00-T88)
    ("S93.401A", "Sprain of unspecified ligament of right ankle, initial encounter"),
    ("S83.90XA", "Sprain of unspecified site of unspecified knee, initial encounter"),
    ("S61.001A", "Unspecified open wound of right thumb without damage to nail, initial encounter"),
    
    # Factors Influencing Health Status (Z00-Z99)
    ("Z00.00", "Encounter for general adult medical examination without abnormal findings"),
    ("Z23", "Encounter for immunization"),
    ("Z96.1", "Presence of intraocular lens"),
    ("Z87.891", "Personal history of nicotine dependence"),
]


def init_database():
    """Initialize the database and populate with ICD-10 codes."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if codes already exist
        existing_count = db.query(DiagnosisCode).count()
        
        if existing_count > 0:
            print(f"Database already contains {existing_count} diagnosis codes.")
            user_input = input("Do you want to reset and repopulate? (y/n): ")
            if user_input.lower() != 'y':
                print("Aborted. Database unchanged.")
                return
            
            # Clear existing codes
            print("Clearing existing diagnosis codes...")
            db.query(DiagnosisCode).delete()
            db.commit()
        
        # Insert ICD-10 codes
        print(f"Inserting {len(ICD10_CODES)} ICD-10 diagnosis codes...")
        
        for code, description in ICD10_CODES:
            diagnosis = DiagnosisCode(code=code, description=description)
            db.add(diagnosis)
        
        db.commit()
        
        # Verify insertion
        final_count = db.query(DiagnosisCode).count()
        print(f"Successfully inserted {final_count} diagnosis codes.")
        
        # Display sample codes
        print("\nSample diagnosis codes:")
        print("-" * 60)
        samples = db.query(DiagnosisCode).limit(10).all()
        for sample in samples:
            print(f"  {sample.code}: {sample.description[:50]}...")
        
        print("\nDatabase initialization complete!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def force_init_database():
    """Force initialize the database without prompts (for automated setup)."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Clear existing codes
        db.query(DiagnosisCode).delete()
        db.commit()
        
        # Insert ICD-10 codes
        print(f"Inserting {len(ICD10_CODES)} ICD-10 diagnosis codes...")
        
        for code, description in ICD10_CODES:
            diagnosis = DiagnosisCode(code=code, description=description)
            db.add(diagnosis)
        
        db.commit()
        
        final_count = db.query(DiagnosisCode).count()
        print(f"Successfully inserted {final_count} diagnosis codes.")
        print("Database initialization complete!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        force_init_database()
    else:
        init_database()
