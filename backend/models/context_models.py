from pydantic import BaseModel, Field
from typing import Optional

class FarmerProfile(BaseModel):
    """
    Session context profile capturing farmer attributes across conversational turns.
    Prevents repeated questioning for previously stated parameters.
    """
    district: Optional[str] = Field(default=None, description="Pakistani district or city (e.g. Multan, Faisalabad)")
    province: str = Field(default="Punjab", description="Province (default Punjab)")
    acres: Optional[float] = Field(default=None, description="Land holding in acres")
    soil_type: Optional[str] = Field(default=None, description="Soil classification (Loam, Clay Loam, Sandy, etc.)")
    current_crop: Optional[str] = Field(default=None, description="Current or planned crop")
    water_source: Optional[str] = Field(default=None, description="Water availability (Canal, Tubewell, Barani, Limited)")
    preferred_language: str = Field(default="Urdu-English", description="Preferred conversational dialect")
