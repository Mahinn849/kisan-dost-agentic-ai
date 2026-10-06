import pytest
from backend.tools.crop_advisor import crop_advisor
from backend.models.crop_models import CropPlan

def test_crop_advisor_rabi_multan():
    """Tests Rabi crop recommendation in Multan on 5 acres with limited water."""
    result: CropPlan = crop_advisor.__wrapped__(
        district="Multan",
        season="Rabi",
        water_availability="limited",
        soil_type="Loam",
        acres=5.0
    )
    assert isinstance(result, CropPlan)
    assert result.status == "success"
    assert len(result.recommendations) > 0
    top_crop_names = [r.crop_name for r in result.recommendations]
    assert any("Wheat" in name or "Gram" in name or "Mustard" in name for name in top_crop_names)
    assert "maunds/acre" in result.recommendations[0].expected_yield_maunds_per_acre

def test_crop_advisor_kharif_canal():
    """Tests Kharif season with abundant canal water in Gujranwala (Rice belt)."""
    result = crop_advisor.__wrapped__(
        district="Gujranwala",
        season="Kharif",
        water_availability="high",
        soil_type="Clay Loam",
        acres=10.0
    )
    assert result.status == "success"
    top_crops = [r.crop_name for r in result.recommendations]
    assert any("Rice" in c for c in top_crops)

def test_crop_advisor_invalid_season():
    """Tests invalid season returns structured error explanation."""
    result = crop_advisor.__wrapped__(
        district="Multan",
        season="SpringAutumnSpecial",
        water_availability="medium",
        soil_type="Loam",
        acres=2.0
    )
    assert result.status == "invalid_season"
    assert len(result.recommendations) == 0
