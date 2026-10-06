import json
from typing import Optional, Dict, Any
from backend.config import CROP_ECONOMICS_PATH
from backend.models.profit_models import ProfitEstimate, CostBreakdown

def load_crop_economics() -> Dict[str, Any]:
    with open(CROP_ECONOMICS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("crops", {})

def estimate_full_season_profit(
    crop: str,
    acres: float,
    expected_yield_per_acre: Optional[float] = None,
    selling_price_per_maund: Optional[float] = None,
    land_preparation_cost: Optional[float] = None,
    seed_cost: Optional[float] = None,
    fertilizer_cost: Optional[float] = None,
    irrigation_cost: Optional[float] = None,
    weed_pest_control_cost: Optional[float] = None,
    harvesting_threshing_cost: Optional[float] = None,
    other_cost: Optional[float] = None
) -> ProfitEstimate:
    """
    Computes a full season farm budget, net margins, and break-even yields.
    Seamlessly utilizes PBS & Agriculture Department Punjab benchmark cost of production
    when farmer provides high-level queries, and accepts explicit custom cost inputs when available.
    """
    crop_clean = crop.lower().strip()
    economics = load_crop_economics()

    matched_key = None
    for key in economics:
        if key in crop_clean or crop_clean in key:
            matched_key = key
            break

    default_benchmark = {
        "crop_name": crop.capitalize(),
        "benchmark_yield_per_acre": 40.0,
        "benchmark_price_per_maund": 3800.0,
        "typical_costs_per_acre": {
            "land_preparation_pkr": 10000,
            "seed_cost_pkr": 6000,
            "fertilizer_cost_pkr": 24000,
            "irrigation_cost_pkr": 14000,
            "weed_pest_control_pkr": 8000,
            "harvesting_threshing_pkr": 15000,
            "other_misc_pkr": 4000
        },
        "total_cost_per_acre": 81000
    }

    econ_data = economics.get(matched_key, default_benchmark)

    # Check if user provided explicit custom inputs
    custom_provided = any(
        v is not None for v in [
            expected_yield_per_acre, selling_price_per_maund, land_preparation_cost,
            seed_cost, fertilizer_cost, irrigation_cost, weed_pest_control_cost,
            harvesting_threshing_cost, other_cost
        ]
    )
    is_benchmark = not custom_provided

    # Resolve yield per acre
    if expected_yield_per_acre is not None and expected_yield_per_acre > 0:
        actual_yield_per_acre = float(expected_yield_per_acre)
    else:
        actual_yield_per_acre = float(econ_data["benchmark_yield_per_acre"])

    # Resolve selling price per maund
    if selling_price_per_maund is not None and selling_price_per_maund > 0:
        actual_price_per_maund = float(selling_price_maund := selling_price_per_maund)
    else:
        actual_price_per_maund = float(econ_data["benchmark_price_per_maund"])

    # Resolve per-acre costs
    typical = econ_data["typical_costs_per_acre"]

    c_land = int(land_preparation_cost * acres) if land_preparation_cost is not None else int(typical["land_preparation_pkr"] * acres)
    c_seed = int(seed_cost * acres) if seed_cost is not None else int(typical["seed_cost_pkr"] * acres)
    c_fert = int(fertilizer_cost * acres) if fertilizer_cost is not None else int(typical["fertilizer_cost_pkr"] * acres)
    c_irri = int(irrigation_cost * acres) if irrigation_cost is not None else int(typical["irrigation_cost_pkr"] * acres)
    c_pest = int(weed_pest_control_cost * acres) if weed_pest_control_cost is not None else int(typical["weed_pest_control_pkr"] * acres)
    c_harv = int(harvesting_threshing_cost * acres) if harvesting_threshing_cost is not None else int(typical["harvesting_threshing_pkr"] * acres)
    c_misc = int(other_cost * acres) if other_cost is not None else int(typical["other_misc_pkr"] * acres)

    total_cost = c_land + c_seed + c_fert + c_irri + c_pest + c_harv + c_misc

    breakdown = CostBreakdown(
        land_preparation_pkr=c_land,
        seed_cost_pkr=c_seed,
        fertilizer_cost_pkr=c_fert,
        irrigation_cost_pkr=c_irri,
        weed_pest_control_pkr=c_pest,
        harvesting_threshing_pkr=c_harv,
        other_misc_pkr=c_misc,
        total_cost_pkr=total_cost
    )

    total_yield = round(actual_yield_per_acre * acres, 2)
    gross_revenue = int(round(total_yield * actual_price_per_maund))
    net_profit = gross_revenue - total_cost

    net_margin_pct = round((net_profit / gross_revenue) * 100.0, 2) if gross_revenue > 0 else 0.0

    cost_per_acre = total_cost / acres if acres > 0 else 0.0
    break_even_yield = round(cost_per_acre / actual_price_per_maund, 2) if actual_price_per_maund > 0 else 0.0

    disclaimer_note = (
        "Projected full season farm financial estimate grounded in Pakistan Bureau of Statistics (PBS) "
        "and Punjab Crop Reporting Service benchmarks. Actual revenues depend on weather outcomes, pest pressure, "
        "and daily mandi market price fluctuations."
    )

    return ProfitEstimate(
        status="calculated",
        crop=econ_data.get("crop_name", crop.capitalize()),
        acres=acres,
        expected_yield_per_acre_maunds=actual_yield_per_acre,
        total_expected_yield_maunds=total_yield,
        selling_price_per_maund_pkr=actual_price_per_maund,
        gross_revenue_pkr=gross_revenue,
        cost_breakdown=breakdown,
        total_cost_pkr=total_cost,
        estimated_net_profit_pkr=net_profit,
        net_margin_percentage=net_margin_pct,
        break_even_yield_maunds_per_acre=break_even_yield,
        is_benchmark_estimate=is_benchmark,
        disclaimer=disclaimer_note
    )
