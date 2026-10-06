from agents import function_tool
from backend.models.crop_models import CropPlan
from backend.services.crop_dataset_service import recommend_crops_for_farm

@function_tool
def crop_advisor(
    district: str,
    season: str,
    water_availability: str,
    soil_type: str,
    acres: float
) -> CropPlan:
    """
    Recommend the best crops for a Pakistani farmer based on district agro-climatic zone,
    season (Rabi / Kharif), water availability (Limited / Medium / High), soil type, and land size.
    Grounded in the Kaggle Crop Recommendation dataset and Directorate of Agriculture Punjab standards.
    Returns structured recommendations with expected yield and financial estimates.
    """
    if acres <= 0:
        acres = 1.0

    return recommend_crops_for_farm(
        district=district,
        season=season,
        water_availability=water_availability,
        soil_type=soil_type,
        acres=acres
    )
