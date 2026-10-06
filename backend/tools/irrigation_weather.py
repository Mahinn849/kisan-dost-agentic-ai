from agents import function_tool
from backend.models.weather_models import WeatherResult
from backend.services.open_meteo_service import fetch_weather_and_irrigation_advisory

@function_tool
def irrigation_weather(
    district: str,
    crop_stage: str
) -> WeatherResult:
    """
    Get live weather forecast and agronomic irrigation advice for a Pakistani district.
    Uses Open-Meteo Geocoding and Weather APIs.
    Evaluates current temperature, humidity, and rainfall against crop growth stage
    (seedling, vegetative, flowering, or maturity) to recommend irrigation timing,
    frost hazard (<4°C), and heatwave warnings (>=40°C).
    Truthful fallback: Returns source/location unavailable if network fails.
    """
    if not district:
        district = "Multan"
    if not crop_stage:
        crop_stage = "vegetative"

    return fetch_weather_and_irrigation_advisory(
        district=district,
        crop_stage=crop_stage
    )
