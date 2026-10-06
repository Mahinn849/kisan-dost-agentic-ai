from agents import function_tool
from backend.models.pest_models import PestDiagnosis
from backend.services.plant_village_service import diagnose_crop_disease

@function_tool
def pest_disease_doctor(
    crop: str,
    symptoms: str
) -> PestDiagnosis:
    """
    Diagnose crop leaf anomalies, insects, and pathological diseases based on farmer symptoms
    (e.g., 'cotton leaves curling, tiny white insects', 'yellow stripes on wheat leaves').
    Grounded in PlantVillage and Agriculture Department Punjab pest databases.
    Provides verified IPM treatments and safe chemical dosages.
    Enforces strict safety: Never guesses unverified pesticide dosage (returns 'dosage_unavailable').
    """
    if not crop:
        crop = "Unknown Crop"
    if not symptoms:
        symptoms = "Unspecified leaf symptoms"

    return diagnose_crop_disease(
        crop=crop,
        symptoms=symptoms
    )
