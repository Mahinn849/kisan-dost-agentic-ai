from agents import function_tool
from backend.models.fertilizer_models import FertilizerPlan
from backend.services.fertilizer_service import compute_fertilizer_plan

@function_tool
def fertilizer_calculator(
    crop: str,
    acres: float
) -> FertilizerPlan:
    """
    Compute total NPK nutrient requirement per acre for a crop and convert it into
    standard 50kg bags of Urea and DAP along with estimated cost in Pakistani Rupees (PKR).
    Provides application scheduling (sowing vs split top-dressing) and soil health advisory.
    """
    if acres <= 0:
        acres = 1.0

    return compute_fertilizer_plan(
        crop=crop,
        acres=acres
    )
