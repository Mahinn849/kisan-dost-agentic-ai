from agents import function_tool
from typing import Optional
from backend.models.profit_models import ProfitEstimate
from backend.services.benchmark_cost_service import estimate_full_season_profit

@function_tool
def profit_estimator(
    crop: str,
    acres: float,
    expected_yield_per_acre: Optional[float] = None,
    selling_price_per_maund: Optional[float] = None,
    land_preparation_cost: Optional[float] = None,
    seed_cost: Optional[float] = None,
    fertilizer_cost: Optional[float] = None,
    labor_cost: Optional[float] = None,
    irrigation_cost: Optional[float] = None,
    other_cost: Optional[float] = None
) -> ProfitEstimate:
    """
    Compute full-season agricultural budget, net profit margin, and break-even yield.
    Calculates input costs (seed, fertilizer, land preparation, labor, irrigation) vs sales revenue.
    Grounded in Pakistan Bureau of Statistics (PBS) and Agriculture Department Punjab economic benchmarks.
    If the farmer does not know detailed cost items, realistic Punjab baseline benchmarks are applied
    and clearly designated as estimates.
    """
    if acres <= 0:
        acres = 1.0

    return estimate_full_season_profit(
        crop=crop,
        acres=acres,
        expected_yield_per_acre=expected_yield_per_acre if (expected_yield_per_acre and expected_yield_per_acre > 0) else None,
        selling_price_per_maund=selling_price_per_maund if (selling_price_per_maund and selling_price_per_maund > 0) else None,
        land_preparation_cost=land_preparation_cost if (land_preparation_cost and land_preparation_cost > 0) else None,
        seed_cost=seed_cost if (seed_cost and seed_cost > 0) else None,
        fertilizer_cost=fertilizer_cost if (fertilizer_cost and fertilizer_cost > 0) else None,
        harvesting_threshing_cost=labor_cost if (labor_cost and labor_cost > 0) else None,
        irrigation_cost=irrigation_cost if (irrigation_cost and irrigation_cost > 0) else None,
        other_cost=other_cost if (other_cost and other_cost > 0) else None
    )
