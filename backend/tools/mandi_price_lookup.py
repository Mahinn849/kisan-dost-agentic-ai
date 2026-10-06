from agents import function_tool
from backend.models.mandi_models import MandiPriceResult
from backend.services.amis_mandi_service import fetch_amis_mandi_price

@function_tool
def mandi_price_lookup(
    crop: str,
    district: str
) -> MandiPriceResult:
    """
    Look up current or latest available wholesale mandi prices for a crop and district
    from official AMIS Punjab (http://www.amis.pk/).
    Returns minimum, maximum, and Fair Quality Price (FQP) per 100 kg and per 40 kg maund.
    Truthful fallback: Never fabricates or estimates live market prices. If quotes are absent,
    reports 'price_not_available'.
    """
    if not crop:
        crop = "Wheat"
    if not district:
        district = "Lahore"

    return fetch_amis_mandi_price(
        crop=crop,
        district=district
    )
