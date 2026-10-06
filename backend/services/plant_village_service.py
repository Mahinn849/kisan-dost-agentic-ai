import json
import re
from typing import List, Dict, Any
from backend.config import PLANT_DISEASES_PATH
from backend.models.pest_models import PestDiagnosis

def load_disease_dataset() -> List[Dict[str, Any]]:
    with open(PLANT_DISEASES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("diseases", [])

def diagnose_crop_disease(crop: str, symptoms: str) -> PestDiagnosis:
    """
    Diagnoses crop leaf anomalies and pest attacks against PlantVillage
    and Agriculture Department Punjab pest databases.
    Enforces strict pesticide dosage safety rules.
    """
    crop_clean = crop.lower().strip()
    symptoms_clean = symptoms.lower().strip()

    diseases = load_disease_dataset()

    best_match = None
    best_score = 0

    # Tokenize farmer symptoms
    tokens = re.findall(r"\w+", symptoms_clean)

    for item in diseases:
        item_crop = item.get("crop", "").lower()

        # Check crop relevance
        crop_match = (item_crop in crop_clean or crop_clean in item_crop)
        if not crop_match:
            continue

        score = 0
        known_symptoms = [s.lower() for s in item.get("symptoms", [])]

        # Check exact multi-word symptom matches
        for s in known_symptoms:
            if s in symptoms_clean:
                score += 15

        # Check individual token overlaps
        for token in tokens:
            if len(token) <= 2:
                continue
            for s in known_symptoms:
                if token in s:
                    score += 4

        if score > best_score:
            best_score = score
            best_match = item

    # If confident match found
    if best_match and best_score >= 12:
        return PestDiagnosis(
            status="diagnosed",
            crop=crop,
            symptoms_analyzed=symptoms,
            likely_problem=best_match["disease_name"],
            disease_type=best_match["type"],
            severity=best_match["severity"],
            treatment=best_match["recommended_treatment"],
            safe_chemical=best_match["safe_chemical"],
            safe_dosage=best_match["safe_dosage"],
            dosage_status=best_match.get("dosage_status", "verified_safe"),
            safety_precautions=best_match["safety_precautions"],
            source=best_match["source"]
        )

    # If crop is known but symptoms are vague or unrecognized
    matched_crop_items = [d for d in diseases if d.get("crop", "").lower() in crop_clean or crop_clean in d.get("crop", "").lower()]
    if matched_crop_items:
        common_problems = ", ".join([d["disease_name"] for d in matched_crop_items[:2]])
        return PestDiagnosis(
            status="uncertain",
            crop=crop,
            symptoms_analyzed=symptoms,
            likely_problem=f"Unconfirmed anomaly in {crop}. Common issues include: {common_problems}.",
            disease_type="Unconfirmed / Requires field verification",
            severity="Medium",
            treatment="Inspect undersides of leaves for sucking insects (nymphs/whiteflies) or check roots for wilting. Avoid applying broad-spectrum pesticides blindly.",
            safe_chemical="Not prescribed until diagnosis is verified.",
            safe_dosage="dosage_unavailable",
            dosage_status="dosage_unavailable",
            safety_precautions="⚠️ SAFETY NOTICE: Safe chemical dosage cannot be determined without definitive pest identification. Do NOT spray unverified chemical formulas. Consult the nearest Agriculture Extension field officer.",
            source="Agriculture Department Punjab Integrated Pest Management (IPM) Directive"
        )

    # General fallback for unlisted crops
    return PestDiagnosis(
        status="unsupported_crop",
        crop=crop,
        symptoms_analyzed=symptoms,
        likely_problem=f"Symptoms on '{crop}' require laboratory or physical field examination.",
        disease_type="Unknown",
        severity="Low to Medium",
        treatment="Isolate affected plants. Take clear leaf photos or physical samples to the local Pest Warning and Quality Control lab.",
        safe_chemical="None",
        safe_dosage="dosage_unavailable",
        dosage_status="dosage_unavailable",
        safety_precautions="Never guess pesticide dosage. Over-application causes phytotoxicity, beneficial pollinator mortality, and groundwater contamination.",
        source="Punjab Plant Protection & Pesticide Safety Rules"
    )
