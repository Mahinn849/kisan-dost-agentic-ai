import pytest
from backend.tools.govt_support_finder import govt_support_finder
from backend.models.support_models import GovtSupportResult

def test_support_punjab_kisan_card():
    """Tests retrieval of CM Punjab Kisan Card scheme."""
    result: GovtSupportResult = govt_support_finder.__wrapped__(
        province="Punjab",
        farmer_need="kisan card"
    )
    assert isinstance(result, GovtSupportResult)
    assert result.status == "success"
    assert len(result.matched_schemes) > 0
    kisan_card = [s for s in result.matched_schemes if "kisan_card" in s.id]
    assert len(kisan_card) > 0
    assert "150,000" in kisan_card[0].benefit
    assert "8070" in kisan_card[0].how_to_apply

def test_support_solar_tubewell():
    """Tests solarization tubewell subsidy retrieval."""
    result = govt_support_finder.__wrapped__(
        province="Punjab",
        farmer_need="solar tubewell"
    )
    assert result.status == "success"
    solar = [s for s in result.matched_schemes if "solar_tubewell" in s.id]
    assert len(solar) > 0
    assert "75%" in solar[0].benefit

def test_support_unsupported_province():
    """Tests truthful response when querying non-Punjab province."""
    result = govt_support_finder.__wrapped__(
        province="Sindh",
        farmer_need="kisan card"
    )
    assert result.status == "unsupported_province"
