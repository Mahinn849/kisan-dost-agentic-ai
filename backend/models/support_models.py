from pydantic import BaseModel, Field
from typing import List

class SchemeDetail(BaseModel):
    id: str = Field(description="Unique scheme identifier")
    scheme_name: str = Field(description="Official scheme title in English and Urdu")
    category: str = Field(description="Scheme category: credit, fertilizer, machinery, solar, insurance")
    target_province: str = Field(description="Geographic applicability")
    benefit: str = Field(description="Financial subsidy, loan terms, or material benefit provided")
    eligibility: str = Field(description="Acreage caps, PLRA land verification, and farmer criteria")
    how_to_apply: str = Field(description="Official application procedure (SMS code, portal, or department office)")
    source_url: str = Field(description="Official Punjab Government verification URL")

class GovtSupportResult(BaseModel):
    status: str = Field(default="success", description="Status code: 'success', 'no_match', 'unsupported_province'")
    province: str = Field(description="Province inquired")
    farmer_need: str = Field(description="Specific assistance area requested by farmer")
    matched_schemes: List[SchemeDetail] = Field(description="Eligible government agricultural programs")
    source: str = Field(default="Agriculture Department, Government of the Punjab", description="Information source")
    notes: str = Field(description="Practical guidance on application deadlines and biometric verification")
