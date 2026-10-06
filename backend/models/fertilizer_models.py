from pydantic import BaseModel, Field

class FertilizerPlan(BaseModel):
    status: str = Field(default="success", description="Calculation status (success, unsupported_crop, etc.)")
    crop: str = Field(description="Target crop name")
    acres: float = Field(description="Total land size in acres")
    nitrogen_req_kg: float = Field(description="Total Nitrogen requirement in kg across land")
    phosphorus_req_kg: float = Field(description="Total Phosphorus requirement in kg across land")
    potassium_req_kg: float = Field(description="Total Potassium requirement in kg across land")
    urea_bags: float = Field(description="Calculated 50kg bags of Urea (46% N)")
    dap_bags: float = Field(description="Calculated 50kg bags of DAP (18% N, 46% P2O5)")
    sop_bags: float = Field(default=0.0, description="Calculated 50kg bags of SOP (50% K2O)")
    urea_cost_pkr: int = Field(description="Total cost for Urea in PKR")
    dap_cost_pkr: int = Field(description="Total cost for DAP in PKR")
    total_cost_pkr: int = Field(description="Total fertilizer expenditure in PKR")
    application_schedule: str = Field(description="Timing and split application advisory (Basal vs Top dressing)")
    notes: str = Field(description="Soil health and efficiency recommendations")
