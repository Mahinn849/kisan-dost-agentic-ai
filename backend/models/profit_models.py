from pydantic import BaseModel, Field

class CostBreakdown(BaseModel):
    land_preparation_pkr: int = Field(description="Tillage, planking, and laser levelling cost in PKR")
    seed_cost_pkr: int = Field(description="Certified seed cost in PKR")
    fertilizer_cost_pkr: int = Field(description="Urea, DAP, and micro-nutrients cost in PKR")
    irrigation_cost_pkr: int = Field(description="Canal abiana and tubewell diesel/electric cost in PKR")
    weed_pest_control_pkr: int = Field(description="Weedicides, fungicides, and pesticide sprays cost in PKR")
    harvesting_threshing_pkr: int = Field(description="Combine harvesting / labor picking cost in PKR")
    other_misc_pkr: int = Field(description="Transportation, bagging, and miscellaneous operational costs in PKR")
    total_cost_pkr: int = Field(description="Sum of all cost inputs across total land area in PKR")

class ProfitEstimate(BaseModel):
    status: str = Field(default="calculated", description="Status code: 'calculated', 'unsupported_crop', 'error'")
    crop: str = Field(description="Crop evaluated")
    acres: float = Field(description="Total acreage")
    expected_yield_per_acre_maunds: float = Field(description="Expected yield per acre in 40 kg maunds")
    total_expected_yield_maunds: float = Field(description="Total harvest production across all acres in maunds")
    selling_price_per_maund_pkr: float = Field(description="Selling price per maund in PKR")
    gross_revenue_pkr: int = Field(description="Total gross sales revenue in PKR")
    cost_breakdown: CostBreakdown = Field(description="Itemized production expenses across total acreage")
    total_cost_pkr: int = Field(description="Total cost of production across all acres in PKR")
    estimated_net_profit_pkr: int = Field(description="Gross revenue minus total cost in PKR")
    net_margin_percentage: float = Field(description="Net profit as percentage of total revenue")
    break_even_yield_maunds_per_acre: float = Field(description="Minimum yield per acre needed to cover total expenses")
    is_benchmark_estimate: bool = Field(description="True if calculated using PBS / Agri Punjab baseline economics, False if custom farmer parameters")
    disclaimer: str = Field(description="Statement clarifying that figures are seasonal projections subject to market volatility")
