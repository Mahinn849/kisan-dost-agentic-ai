from pydantic import BaseModel, Field
from typing import Optional

class MandiPriceResult(BaseModel):
    status: str = Field(description="Status code: 'success', 'price_not_available', 'district_not_found', 'unsupported_crop', 'source_unavailable', 'timeout'")
    crop: str = Field(description="Crop commodity name")
    district: str = Field(description="Market / district queried")
    commodity_id: Optional[int] = Field(default=None, description="Official AMIS commodity ID")
    minimum_price_pkr_per_100kg: Optional[int] = Field(default=None, description="Minimum wholesale price per 100 kg in PKR")
    maximum_price_pkr_per_100kg: Optional[int] = Field(default=None, description="Maximum wholesale price per 100 kg in PKR")
    fqp_price_pkr_per_100kg: Optional[int] = Field(default=None, description="FAQ / Fair Quality Price per 100 kg in PKR")
    price_per_maund_pkr: Optional[int] = Field(default=None, description="Converted price per standard Pakistani maund (40 kg) in PKR")
    unit: str = Field(default="PKR per 100 kg and PKR per 40 kg maund", description="Price quotation unit")
    source: str = Field(default="AMIS Punjab (http://www.amis.pk/)", description="Official data source")
    retrieved_at: Optional[str] = Field(default=None, description="Timestamp or date when price data was accessed")
    message: Optional[str] = Field(default=None, description="Explanatory human-readable note if data is unavailable or filtered")
