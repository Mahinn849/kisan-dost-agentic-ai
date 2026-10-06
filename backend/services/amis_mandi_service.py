import re
import datetime
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Tuple
from backend.config import AMIS_BASE_URL, REQUEST_TIMEOUT_SECONDS, DEFAULT_USER_AGENT
from backend.models.mandi_models import MandiPriceResult

# Real AMIS commodity IDs verified directly from http://www.amis.pk/BrowsePrices.aspx?searchType=0
COMMODITY_MAPPING: Dict[str, Tuple[int, str]] = {
    "wheat": (1, "Wheat"),
    "gandum": (1, "Wheat"),
    "rice": (57, "Rice Basmati Super (Old)"),
    "chawal": (57, "Rice Basmati Super (Old)"),
    "basmati": (57, "Rice Basmati Super (Old)"),
    "rice_irri": (4, "Rice (IRRI)"),
    "cotton": (49, "Seed Cotton (Phutti)"),
    "kapas": (49, "Seed Cotton (Phutti)"),
    "phutti": (49, "Seed Cotton (Phutti)"),
    "maize": (17, "Maize"),
    "corn": (17, "Maize"),
    "makai": (17, "Maize"),
    "potato": (21, "Potato Fresh"),
    "aloo": (21, "Potato Fresh"),
    "potato_store": (22, "Potato Store"),
    "onion": (23, "Onion"),
    "piaz": (23, "Onion"),
    "tomato": (26, "Tomato"),
    "tamatar": (26, "Tomato"),
    "sugarcane": (125, "sugarcane( )"),
    "kamad": (125, "sugarcane( )"),
    "ganna": (125, "sugarcane( )"),
    "gram": (9, "Gram Black Bareek"),
    "chana": (9, "Gram Black Bareek"),
    "chickpea": (8, "Gram White Bareek"),
    "mustard": (122, "Mustard seed"),
    "sarson": (122, "Mustard seed"),
    "sunflower": (116, "Sunflower"),
    "canola": (117, "Canola"),
    "chilli": (29, "Red Chilli Whole (Dry)"),
    "green_chilli": (84, "Green Chilli"),
    "garlic": (32, "Garlic (Local)")
}

# Common Punjab district aliases for resilient matching
DISTRICT_ALIASES: Dict[str, str] = {
    "faisalabad": "faisalabad",
    "lahore": "lahore",
    "multan": "multan",
    "rawalpindi": "rawalpindi",
    "okara": "okara",
    "sahiwal": "sahiwal",
    "sargodha": "sargodha",
    "gujranwala": "gujranwala",
    "bahawalpur": "bahawalpur",
    "rahim yar khan": "rahimyar khan",
    "rahimyar khan": "rahimyar khan",
    "ryk": "rahimyar khan",
    "jhang": "jhang",
    "khanewal": "khanewal",
    "kasur": "kasur",
    "sheikhupura": "sheikhupura",
    "sialkot": "sialkot",
    "vehari": "vehari",
    "bahawalnagar": "bahawalnagar",
    "dg khan": "dg khan",
    "d.g. khan": "dg khan",
    "dera ghazi khan": "dg khan",
    "tt singh": "ttsingh",
    "toba tek singh": "ttsingh",
    "ttsingh": "ttsingh",
    "chichawatni": "chichawatni",
    "pakpattan": "pakpattan",
    "mianwali": "mianwali",
    "bhakkar": "bhakkar",
    "layyah": "layyah",
    "gujrat": "gujrat",
    "mandi bahauddin": "m.b.din",
    "mb din": "m.b.din"
}

def normalize_district_name(district: str) -> str:
    cleaned = district.lower().strip()
    # Remove redundant suffixes like "district", "city", "mandi"
    cleaned = re.sub(r"\b(district|city|mandi|bazar)\b", "", cleaned).strip()
    return DISTRICT_ALIASES.get(cleaned, cleaned)

def fetch_amis_mandi_price(crop: str, district: str) -> MandiPriceResult:
    """
    Scrapes real-time wholesale mandi rates from AMIS Punjab (http://www.amis.pk/).
    Strictly preserves HTTP protocol. Never fabricates prices.
    """
    crop_clean = crop.lower().strip()
    district_clean = district.lower().strip()
    norm_district = normalize_district_name(district_clean)

    # Resolve commodity
    matched_crop_key = None
    for key in COMMODITY_MAPPING:
        if key in crop_clean or crop_clean in key:
            matched_crop_key = key
            break

    if not matched_crop_key:
        supported = ", ".join(["Wheat", "Rice", "Cotton", "Maize", "Potato", "Onion", "Tomato", "Sugarcane", "Gram", "Mustard", "Sunflower"])
        return MandiPriceResult(
            status="unsupported_crop",
            crop=crop,
            district=district,
            message=f"Commodity '{crop}' is not currently configured for AMIS lookup. Supported crops include: {supported}."
        )

    commodity_id, official_name = COMMODITY_MAPPING[matched_crop_key]
    amis_url = f"{AMIS_BASE_URL}/ViewPrices.aspx?commodityId={commodity_id}&searchType=0"

    headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        response = requests.get(amis_url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract date from page input if present
        date_input = soup.find("input", {"id": re.compile(r"Date", re.I)})
        date_str = date_input.get("value") if date_input else datetime.date.today().strftime("%d-%m-%Y")

        target_row = None
        # Parse table rows
        for row in soup.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in row.find_all(["td", "th"])]
            if len(cells) < 5:
                continue

            first_cell = cells[0].strip()
            # Match number followed by city (e.g. "1 Lahore", "2 Faisalabad")
            num_match = re.match(r"^\s*\d+\s+(.+?)\s*$", first_cell)
            if not num_match:
                continue

            city_text = num_match.group(1).strip().lower()
            city_norm = normalize_district_name(city_text)

            if norm_district in city_norm or city_norm in norm_district:
                target_row = cells
                break

        if not target_row:
            return MandiPriceResult(
                status="district_not_found",
                crop=official_name,
                district=district,
                commodity_id=commodity_id,
                retrieved_at=date_str,
                message=f"'{district}' was not found in the official AMIS market list for {official_name}."
            )

        # Structure of AMIS row: [0]=City, [1]=Graph, [2]=Min, [3]=Max, [4]=FQP, [5]=Quantity
        min_str = target_row[2].replace(",", "").strip() if len(target_row) > 2 else "-"
        max_str = target_row[3].replace(",", "").strip() if len(target_row) > 3 else "-"
        fqp_str = target_row[4].replace(",", "").strip() if len(target_row) > 4 else "-"

        # If data is unquoted or empty ("-")
        if min_str == "-" or max_str == "-" or fqp_str == "-":
            return MandiPriceResult(
                status="price_not_available",
                crop=official_name,
                district=district,
                commodity_id=commodity_id,
                retrieved_at=date_str,
                message=f"AMIS Punjab has an active market record for {district}, but no wholesale trades or price quotes were posted for {official_name} today ({date_str})."
            )

        try:
            min_price = int(min_str)
            max_price = int(max_str)
            fqp_price = int(fqp_str)
            # 1 maund in Pakistan = 40 kg. Price is per 100 kg.
            maund_price = int(round((fqp_price / 100.0) * 40.0))

            return MandiPriceResult(
                status="success",
                crop=official_name,
                district=district,
                commodity_id=commodity_id,
                minimum_price_pkr_per_100kg=min_price,
                maximum_price_pkr_per_100kg=max_price,
                fqp_price_pkr_per_100kg=fqp_price,
                price_per_maund_pkr=maund_price,
                retrieved_at=date_str,
                message=f"Successfully retrieved live AMIS wholesale price for {official_name} in {district} mandi."
            )
        except ValueError:
            return MandiPriceResult(
                status="parse_error",
                crop=official_name,
                district=district,
                commodity_id=commodity_id,
                retrieved_at=date_str,
                message=f"Received non-numeric price format from AMIS table: min={min_str}, max={max_str}, fqp={fqp_str}."
            )

    except requests.exceptions.Timeout:
        return MandiPriceResult(
            status="timeout",
            crop=crop,
            district=district,
            message="AMIS Punjab server (http://www.amis.pk/) timed out. Please try again shortly."
        )
    except requests.exceptions.RequestException as e:
        return MandiPriceResult(
            status="source_unavailable",
            crop=crop,
            district=district,
            message=f"Could not reach AMIS Punjab server: {str(e)}"
        )
    except Exception as e:
        return MandiPriceResult(
            status="error",
            crop=crop,
            district=district,
            message=f"Unexpected error while parsing AMIS mandi data: {str(e)}"
        )
