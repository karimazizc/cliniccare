"""Initialize database with ICD-10 diagnosis codes."""

from database import engine, SessionLocal, Base
from models import DiagnosisCode, Consultation

# 100 ICD-10 Codes — Certain Infectious and Parasitic Diseases (A00-B99)
ICD10_CODES = [
    # Intestinal Infectious Diseases (A00-A09)
    ("A00.0", "Cholera due to Vibrio cholerae 01, biovar cholerae"),
    ("A00.1", "Cholera due to Vibrio cholerae 01, biovar eltor"),
    ("A00.9", "Cholera, unspecified"),
    ("A01.0", "Typhoid fever"),
    ("A01.1", "Paratyphoid fever A"),
    ("A01.2", "Paratyphoid fever B"),
    ("A01.3", "Paratyphoid fever C"),
    ("A01.4", "Paratyphoid fever, unspecified"),
    ("A02.0", "Salmonella enteritis"),
    ("A02.1", "Salmonella sepsis"),
    ("A03.0", "Shigellosis due to Shigella dysenteriae"),
    ("A03.9", "Shigellosis, unspecified"),
    ("A04.0", "Enteropathogenic Escherichia coli infection"),
    ("A04.5", "Campylobacter enteritis"),
    ("A04.7", "Enterocolitis due to Clostridium difficile"),
    ("A04.72", "Enterocolitis due to Clostridium difficile, recurrent"),
    ("A05.1", "Botulism food poisoning"),
    ("A06.0", "Acute amebic dysentery"),
    ("A06.9", "Amebiasis, unspecified"),
    ("A07.1", "Giardiasis [lambliasis]"),
    ("A08.0", "Rotaviral enteritis"),
    ("A08.11", "Acute gastroenteropathy due to Norwalk agent"),
    ("A09", "Infectious gastroenteritis and colitis, unspecified"),

    # Tuberculosis (A15-A19)
    ("A15.0", "Tuberculosis of lung"),
    ("A15.5", "Tuberculosis of larynx, trachea and bronchus"),
    ("A15.6", "Tuberculous pleurisy"),
    ("A15.9", "Respiratory tuberculosis, unspecified"),
    ("A17.0", "Tuberculous meningitis"),
    ("A18.2", "Tuberculous peripheral lymphadenopathy"),
    ("A19.0", "Acute miliary tuberculosis of a single specified site"),
    ("A19.9", "Miliary tuberculosis, unspecified"),

    # Certain Zoonotic Bacterial Diseases (A20-A28)
    ("A20.0", "Bubonic plague"),
    ("A22.1", "Pulmonary anthrax"),
    ("A23.9", "Brucellosis, unspecified"),
    ("A27.0", "Leptospirosis icterohemorrhagica"),
    ("A27.9", "Leptospirosis, unspecified"),

    # Other Bacterial Diseases (A30-A49)
    ("A30.9", "Leprosy [Hansen disease], unspecified"),
    ("A31.0", "Pulmonary mycobacterial infection"),
    ("A32.7", "Listerial sepsis"),
    ("A33", "Tetanus neonatorum"),
    ("A35", "Other tetanus"),
    ("A36.0", "Pharyngeal diphtheria"),
    ("A37.90", "Whooping cough, unspecified species without pneumonia"),
    ("A38.9", "Scarlet fever, uncomplicated"),
    ("A39.0", "Meningococcal meningitis"),
    ("A40.0", "Sepsis due to streptococcus, group A"),
    ("A41.01", "Sepsis due to Methicillin susceptible Staphylococcus aureus"),
    ("A41.02", "Sepsis due to Methicillin resistant Staphylococcus aureus"),
    ("A41.9", "Sepsis, unspecified organism"),
    ("A46", "Erysipelas"),
    ("A48.0", "Gas gangrene"),
    ("A49.01", "Methicillin susceptible Staphylococcus aureus infection, unspecified site"),
    ("A49.02", "Methicillin resistant Staphylococcus aureus infection, unspecified site"),

    # Infections with a Predominantly Sexual Mode of Transmission (A50-A64)
    ("A50.9", "Congenital syphilis, unspecified"),
    ("A51.0", "Primary genital syphilis"),
    ("A53.9", "Syphilis, unspecified"),
    ("A54.00", "Gonococcal infection of lower genitourinary tract, unspecified"),
    ("A56.0", "Chlamydial infection of lower genitourinary tract"),
    ("A56.2", "Chlamydial infection of genitourinary tract, unspecified"),
    ("A59.9", "Trichomoniasis, unspecified"),
    ("A60.00", "Herpesviral infection of urogenital system, unspecified"),
    ("A63.0", "Anogenital (venereal) warts"),

    # Other Spirochetal Diseases (A65-A69)
    ("A69.20", "Lyme disease, unspecified"),
    ("A69.21", "Meningitis due to Lyme disease"),
    ("A69.29", "Other conditions associated with Lyme disease"),

    # Other Diseases Caused by Chlamydiae (A70-A74)
    ("A70", "Chlamydia psittaci infections"),
    ("A71.9", "Trachoma, unspecified"),

    # Rickettsioses (A75-A79)
    ("A77.0", "Spotted fever due to Rickettsia rickettsii"),
    ("A79.9", "Rickettsiosis, unspecified"),

    # Viral and Prion Infections of the Central Nervous System (A80-A89)
    ("A80.9", "Acute poliomyelitis, unspecified"),
    ("A81.0", "Creutzfeldt-Jakob disease"),
    ("A82.9", "Rabies, unspecified"),
    ("A84.9", "Tick-borne viral encephalitis, unspecified"),
    ("A86", "Unspecified viral encephalitis"),
    ("A87.9", "Viral meningitis, unspecified"),

    # Arthropod-Borne Viral Fevers and Viral Hemorrhagic Fevers (A90-A99)
    ("A90", "Dengue fever [classical dengue]"),
    ("A91", "Dengue hemorrhagic fever"),
    ("A92.5", "Zika virus disease"),
    ("A95.9", "Yellow fever, unspecified"),
    ("A97.0", "Dengue without warning signs"),

    # Viral Infections Characterized by Skin and Mucous Membrane Lesions (B00-B09)
    ("B00.1", "Herpesviral vesicular dermatitis"),
    ("B00.9", "Herpesviral infection, unspecified"),
    ("B01.9", "Varicella without complication"),
    ("B02.9", "Zoster without complications"),
    ("B05.9", "Measles without complication"),
    ("B06.9", "Rubella without complication"),
    ("B07.9", "Viral wart, unspecified"),
    ("B08.4", "Enteroviral vesicular stomatitis with exanthem"),
    ("B09", "Unspecified viral infection characterized by skin and mucous membrane lesions"),

    # Viral Hepatitis (B15-B19)
    ("B15.9", "Hepatitis A without hepatic coma"),
    ("B16.9", "Acute hepatitis B without delta-agent and without hepatic coma"),
    ("B17.10", "Acute hepatitis C without hepatic coma"),
    ("B18.1", "Chronic viral hepatitis B without delta-agent"),
    ("B18.2", "Chronic viral hepatitis C"),
    ("B19.9", "Unspecified viral hepatitis without hepatic coma"),

    # HIV Disease (B20)
    ("B20", "Human immunodeficiency virus [HIV] disease"),

    # Other Viral Diseases (B25-B34)
    ("B25.9", "Cytomegaloviral disease, unspecified"),
    ("B26.9", "Mumps without complication"),
    ("B27.00", "Gammaherpesviral mononucleosis without complication"),
    ("B34.9", "Viral infection, unspecified"),
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
