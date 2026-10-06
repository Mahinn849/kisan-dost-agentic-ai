from pydantic import BaseModel, Field
from typing import Optional

class WeatherResult(BaseModel):
    status: str = Field(description="Query status: 'live', 'location_not_found', 'source_unavailable', 'timeout', etc.")
    district: str = Field(description="Requested Pakistani district or city")
    resolved_location: str = Field(description="Resolved location name from geocoding API")
    latitude: Optional[float] = Field(default=None, description="Geographic latitude")
    longitude: Optional[float] = Field(default=None, description="Geographic longitude")
    crop_stage: str = Field(description="Growth stage: seedling, vegetative, flowering, or maturity")
    current_temperature_c: Optional[float] = Field(default=None, description="Current ambient temperature in Celsius")
    relative_humidity_pct: Optional[int] = Field(default=None, description="Current relative humidity percentage")
    max_temperature_c: Optional[float] = Field(default=None, description="Forecasted maximum temperature today")
    min_temperature_c: Optional[float] = Field(default=None, description="Forecasted minimum temperature today")
    expected_rain_mm: Optional[float] = Field(default=None, description="Forecasted precipitation sum in millimeters")
    frost_warning: bool = Field(default=False, description="Alert if minimum temperature drops below 4°C")
    heatwave_warning: bool = Field(default=False, description="Alert if temperature exceeds 40°C")
    irrigation_advisory: str = Field(description="Tailored irrigation timing recommendation based on rain and stage")
    hazard_warning: str = Field(description="Detailed frost, heatwave, or waterlogging alert")
    source: str = Field(default="Open-Meteo Weather API", description="External weather data provider")
    message: Optional[str] = Field(default=None, description="Diagnostic or fallback explanation if live data unavailable")
