from agents import function_tool
from backend.models.support_models import GovtSupportResult
from backend.services.punjab_agri_service import find_govt_support

@function_tool
def govt_support_finder(
    province: str,
    farmer_need: str
) -> GovtSupportResult:
    """
    Surface official Government of the Punjab agriculture support programs, including:
    - CM Punjab Kisan Card (interest-free production credit lines up to PKR 150,000 via BOP)
    - Subsidized Fertilizer / DAP Scratch-Card Vouchers
    - Chief Minister Green Tractor Scheme
    - Solarization of Agricultural Tubewells (75% subsidy)
    - Crop Loan Insurance (CLIS / Takaful)
    Grounded in official Punjab Agriculture Department (https://www.agripunjab.gov.pk/) data.
    """
    if not province:
        province = "Punjab"
    if not farmer_need:
        farmer_need = "all"

    return find_govt_support(
        province=province,
        farmer_need=farmer_need
    )
