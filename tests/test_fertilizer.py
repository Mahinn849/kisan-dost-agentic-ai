import pytest
from backend.tools.fertilizer_calculator import fertilizer_calculator
from backend.models.fertilizer_models import FertilizerPlan

def test_fertilizer_wheat_5_acres():
    """Tests fertilizer computation for 5 acres of wheat."""
    result: FertilizerPlan = fertilizer_calculator.__wrapped__("Wheat", 5.0)
    assert isinstance(result, FertilizerPlan)
    assert result.status == "success"
    assert result.acres == 5.0
    assert result.urea_bags > 0
    assert result.dap_bags > 0
    assert result.total_cost_pkr == (result.urea_cost_pkr + result.dap_cost_pkr)
    assert len(result.application_schedule) > 0

def test_fertilizer_zero_or_negative_acres():
    """Tests graceful boundary handling for invalid acreage."""
    result = fertilizer_calculator.__wrapped__("Cotton", 0.0)
    assert result.status == "success"
    assert result.acres == 1.0  # Normalized to 1.0 baseline
    assert result.urea_bags > 0

def test_fertilizer_uncommon_crop():
    """Tests fallback to standard baseline nutrient dosing for uncommon crops."""
    result = fertilizer_calculator.__wrapped__("Sunflower", 3.0)
    assert result.status == "success"
    assert result.total_cost_pkr > 0
