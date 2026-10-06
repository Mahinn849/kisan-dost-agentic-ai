import pytest
from backend.tools.profit_estimator import profit_estimator
from backend.models.profit_models import ProfitEstimate

def test_profit_estimator_wheat_benchmark():
    """Tests full season budget using PBS & Agri Punjab benchmarks for 5 acres of wheat."""
    result: ProfitEstimate = profit_estimator.__wrapped__(
        crop="Wheat",
        acres=5.0
    )
    assert isinstance(result, ProfitEstimate)
    assert result.status == "calculated"
    assert result.acres == 5.0
    assert result.gross_revenue_pkr > 0
    assert result.total_cost_pkr > 0
    assert result.estimated_net_profit_pkr == (result.gross_revenue_pkr - result.total_cost_pkr)
    assert result.break_even_yield_maunds_per_acre > 0
    assert result.is_benchmark_estimate is True
    assert "PBS" in result.disclaimer or "Pakistan Bureau of Statistics" in result.disclaimer

def test_profit_estimator_custom_values():
    """Tests profit calculation with farmer's explicit cost inputs."""
    result = profit_estimator.__wrapped__(
        crop="Cotton",
        acres=2.0,
        expected_yield_per_acre=30.0,
        selling_price_per_maund=8000.0,
        seed_cost=5000.0,
        fertilizer_cost=25000.0,
        labor_cost=15000.0,
        irrigation_cost=10000.0,
        other_cost=5000.0
    )
    assert result.status == "calculated"
    assert result.total_expected_yield_maunds == 60.0
    assert result.gross_revenue_pkr == 480000
    assert result.is_benchmark_estimate is False
