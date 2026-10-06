import pytest
from backend.tools.pest_disease_doctor import pest_disease_doctor
from backend.models.pest_models import PestDiagnosis

def test_pest_cotton_whitefly():
    """Tests cotton whitefly diagnosis with safe dosage from PlantVillage / Agri Punjab."""
    result: PestDiagnosis = pest_disease_doctor.__wrapped__("Cotton", "leaves curling, tiny white insects on lower surface")
    assert isinstance(result, PestDiagnosis)
    assert result.status == "diagnosed"
    assert "Whitefly" in result.likely_problem
    assert result.dosage_status == "verified_safe"
    assert "200-250 ml" in result.safe_dosage
    assert len(result.safety_precautions) > 0

def test_pest_wheat_rust():
    """Tests wheat yellow rust diagnosis."""
    result = pest_disease_doctor.__wrapped__("Wheat", "yellow stripes powdery pustules on leaves")
    assert result.status == "diagnosed"
    assert "Rust" in result.likely_problem
    assert result.dosage_status == "verified_safe"

def test_pest_unknown_symptom_safe_dosage_unavailable():
    """Critical safety test: unknown symptom must NOT invent dosage (returns dosage_unavailable)."""
    result = pest_disease_doctor.__wrapped__("Wheat", "strange alien glowing purple spots")
    assert result.status == "uncertain"
    assert result.dosage_status == "dosage_unavailable"
    assert result.safe_dosage == "dosage_unavailable"
    assert "Do NOT spray unverified chemical" in result.safety_precautions

def test_pest_unsupported_crop():
    """Tests unsupported crop returns safe refusal without guessing."""
    result = pest_disease_doctor.__wrapped__("Pineapple", "black leaf edges")
    assert result.status == "unsupported_crop"
    assert result.dosage_status == "dosage_unavailable"
