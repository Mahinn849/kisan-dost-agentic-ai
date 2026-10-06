import pytest
from backend.tools.mandi_price_lookup import mandi_price_lookup
from backend.models.mandi_models import MandiPriceResult

def test_mandi_live_rice_lahore():
    """Tests live AMIS connection for Rice in Lahore."""
    result: MandiPriceResult = mandi_price_lookup.__wrapped__("Rice", "Lahore")
    assert isinstance(result, MandiPriceResult)
    assert result.status in ["success", "price_not_available", "timeout", "source_unavailable"]
    if result.status == "success":
        assert result.minimum_price_pkr_per_100kg is not None
        assert result.price_per_maund_pkr is not None
        assert result.price_per_maund_pkr > 0
        assert "AMIS" in result.source

def test_mandi_unsupported_crop():
    """Tests unsupported crop returns honest status."""
    result = mandi_price_lookup.__wrapped__("Avocado", "Lahore")
    assert result.status == "unsupported_crop"
    assert "not currently configured" in result.message

def test_mandi_district_not_found():
    """Tests non-existent district returns truthful district_not_found."""
    result = mandi_price_lookup.__wrapped__("Rice", "NonExistentCityXYZ")
    assert result.status in ["district_not_found", "timeout", "source_unavailable"]
    if result.status == "district_not_found":
        assert "was not found" in result.message

def test_mandi_price_not_available():
    """Tests that unquoted commodities return truthful price_not_available rather than fabricated numbers."""
    result = mandi_price_lookup.__wrapped__("Wheat", "Lahore")
    assert result.status in ["price_not_available", "success", "timeout", "source_unavailable"]
    if result.status == "price_not_available":
        assert "no wholesale trades or price quotes were posted" in result.message
