from pydantic import BaseModel, Field
from typing import List

class CropRecommendationItem(BaseModel):
    crop_name: str = Field(description="Name of the recommended crop in English")
    urdu_name: str = Field(description="Urdu vernacular name")
    expected_yield_maunds_per_acre: str = Field(description="Expected yield range in maunds (40 kg)")
    estimated_gross_revenue_pkr_per_acre: str = Field(description="Projected gross revenue range per acre in PKR")
    estimated_net_profit_pkr_per_acre: str = Field(description="Projected net profit range per acre in PKR")
    suitability_reason: str = Field(description="Agronomic justification based on soil, district, water, and season")

class CropPlan(BaseModel):
    status: str = Field(default="success", description="Status of the recommendation")
    district: str = Field(description="Farmer's district")
    season: str = Field(description="Season (Rabi or Kharif)")
    acres: float = Field(description="Land size in acres")
    recommendations: List[CropRecommendationItem] = Field(description="Ranked list of crop recommendations")
    advisory_notes: str = Field(description="Expert agronomic guidance for crop selection")
