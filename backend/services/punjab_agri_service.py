import json
from typing import List, Dict, Any
from backend.config import PUNJAB_SCHEMES_PATH
from backend.models.support_models import GovtSupportResult, SchemeDetail

def load_punjab_schemes() -> List[Dict[str, Any]]:
    with open(PUNJAB_SCHEMES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("schemes", [])

def find_govt_support(province: str, farmer_need: str) -> GovtSupportResult:
    """
    Finds verified Punjab agricultural schemes, subsidies, and credit facilities
    grounded in official Agriculture Department Punjab guidelines.
    """
    prov_clean = province.strip().lower()
    need_clean = farmer_need.strip().lower()

    if "punjab" not in prov_clean:
        return GovtSupportResult(
            status="unsupported_province",
            province=province,
            farmer_need=farmer_need,
            matched_schemes=[],
            source="Agriculture Department Punjab",
            notes=f"Kisan Dost currently provides verified provincial schemes for Punjab. Federal programs like Kamyab Kisan and PM Agriculture Package may apply in {province.capitalize()}."
        )

    all_schemes = load_punjab_schemes()
    matched: List[SchemeDetail] = []

    # Keywords mapping
    need_keywords = {
        "kisan_card": ["card", "credit", "loan", "qarz", "seed", "paisa", "input", "interest free", "interest-free"],
        "fertilizer_subsidy": ["fertilizer", "khad", "dap", "urea", "voucher", "subsidy", "potash"],
        "green_tractor": ["tractor", "machinery", "machine", "implement", "hal", "cultivator"],
        "solar_tubewell": ["solar", "tubewell", "tube well", "electricity", "diesel", "irrigation", "bijli", "solarization"],
        "crop_insurance": ["insurance", "beema", "takaful", "loss", "flood", "disaster", "drought", "risk"]
    }

    # Match specific needs
    for scheme in all_schemes:
        s_id = scheme["id"]
        keywords = need_keywords.get(s_id, [])

        is_match = False
        for kw in keywords:
            if kw in need_clean:
                is_match = True
                break

        if is_match or "all" in need_clean or "support" in need_clean or "scheme" in need_clean or "help" in need_clean or not need_clean:
            matched.append(
                SchemeDetail(
                    id=scheme["id"],
                    scheme_name=scheme["scheme_name"],
                    category=scheme["category"],
                    target_province=scheme["target_province"],
                    benefit=scheme["benefit"],
                    eligibility=scheme["eligibility"],
                    how_to_apply=scheme["how_to_apply"],
                    source_url=scheme["source_url"]
                )
            )

    # If nothing matched specifically, provide top flagship schemes
    if not matched:
        matched = [
            SchemeDetail(
                id=s["id"],
                scheme_name=s["scheme_name"],
                category=s["category"],
                target_province=s["target_province"],
                benefit=s["benefit"],
                eligibility=s["eligibility"],
                how_to_apply=s["how_to_apply"],
                source_url=s["source_url"]
            )
            for s in all_schemes[:3]
        ]

    return GovtSupportResult(
        status="success",
        province=province,
        farmer_need=farmer_need,
        matched_schemes=matched,
        source="Agriculture Department, Government of the Punjab (https://www.agripunjab.gov.pk/)",
        notes="Farmers must ensure their land records are updated in the Punjab Land Records Authority (PLRA) computer system for biometric verification."
    )
