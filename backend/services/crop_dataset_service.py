import json
from typing import List, Dict, Any
from backend.config import CROP_RECOMMENDATION_PATH, CROP_ECONOMICS_PATH
from backend.models.crop_models import CropPlan, CropRecommendationItem

def load_crop_dataset() -> List[Dict[str, Any]]:
    with open(CROP_RECOMMENDATION_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("crops", [])

def load_crop_economics() -> Dict[str, Any]:
    with open(CROP_ECONOMICS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("crops", {})

def recommend_crops_for_farm(
    district: str,
    season: str,
    water_availability: str,
    soil_type: str,
    acres: float
) -> CropPlan:
    """
    Evaluates grounded agro-climatic parameters from Kaggle Crop Recommendation
    and Agriculture Department Punjab guidelines to recommend optimal crops.
    """
    district_clean = district.strip()
    season_clean = season.strip().capitalize()
    water_clean = water_availability.strip().lower()
    soil_clean = soil_type.strip().lower()

    if season_clean not in ["Rabi", "Kharif"]:
        if "winter" in season.lower():
            season_clean = "Rabi"
        elif "summer" in season.lower() or "monsoon" in season.lower():
            season_clean = "Kharif"
        else:
            return CropPlan(
                status="invalid_season",
                district=district,
                season=season,
                acres=acres,
                recommendations=[],
                advisory_notes=f"Unrecognized season '{season}'. Pakistan agriculture relies on two distinct seasons: 'Rabi' (Winter, Oct-April) and 'Kharif' (Summer, May-Nov)."
            )

    all_crops = load_crop_dataset()
    economics = load_crop_economics()

    candidates = []

    for crop in all_crops:
        if crop.get("season", "").capitalize() != season_clean:
            continue

        score = 0
        crop_water = crop.get("water_requirement", "").lower()
        suitable_soils = [s.lower() for s in crop.get("suitable_soils", [])]
        districts = [d.lower() for d in crop.get("suitable_districts", [])]

        # 1. Water compatibility scoring
        if "limited" in water_clean or "low" in water_clean or "barani" in water_clean:
            if crop_water == "low":
                score += 40
            elif crop_water == "medium":
                score += 15
            else:  # High water crop like rice or sugarcane in limited water
                score -= 50
        elif "high" in water_clean or "canal" in water_clean or "abundant" in water_clean:
            if crop_water == "high":
                score += 35
            elif crop_water == "medium":
                score += 30
            else:
                score += 15
        else:  # Medium water
            if crop_water in ["medium", "low"]:
                score += 30
            else:
                score += 10

        # 2. Soil compatibility scoring
        soil_match = False
        for s in suitable_soils:
            if s in soil_clean or soil_clean in s or "loam" in soil_clean:
                soil_match = True
                break
        if soil_match:
            score += 25

        # 3. District agro-ecological zone match
        dist_match = False
        for d in districts:
            if d in district_clean.lower() or district_clean.lower() in d:
                dist_match = True
                break
        if dist_match:
            score += 25

        if score > 0:
            candidates.append((score, crop))

    # Rank by suitability score
    candidates.sort(key=lambda x: x[0], reverse=True)
    top_candidates = candidates[:3] if candidates else []

    recommendation_items: List[CropRecommendationItem] = []

    # Map economics
    econ_lookup = {
        "wheat": "wheat",
        "cotton": "cotton",
        "rice (basmati)": "rice_basmati",
        "rice (irri / coarse)": "rice_coarse",
        "maize (spring / autumn)": "maize",
        "gram (chickpea / chana)": "gram",
        "potato": "potato",
        "sugarcane": "sugarcane"
    }

    for score, crop in top_candidates:
        c_name = crop["name"]
        u_name = crop.get("urdu_name", c_name)
        yield_info = crop.get("expected_yield_maunds_per_acre", {})
        yield_str = f"{yield_info.get('min', 30)}-{yield_info.get('max', 45)} maunds/acre (Avg: {yield_info.get('avg', 38)})"

        # Financial projections
        key = econ_lookup.get(c_name.lower())
        if key and key in economics:
            econ = economics[key]
            avg_yield = yield_info.get("avg", econ.get("benchmark_yield_per_acre", 35))
            maund_price = econ.get("benchmark_price_per_maund", 3500)
            cost_per_acre = econ.get("total_cost_per_acre", 65000)

            gross_pkr = int(round(avg_yield * maund_price))
            net_pkr = int(round(gross_pkr - cost_per_acre))

            gross_str = f"PKR {gross_pkr:,} / acre"
            net_str = f"PKR {net_pkr:,} / acre (Estimated Margin)"
        else:
            gross_str = "PKR 120,000 - 180,000 / acre (Estimated)"
            net_str = "PKR 50,000 - 90,000 / acre (Estimated)"

        reason_parts = []
        if score >= 60:
            reason_parts.append(f"Highly suited for {district_clean}'s agro-climatic zone.")
        if "limited" in water_clean and crop.get("water_requirement", "").lower() == "low":
            reason_parts.append("Excels under constrained irrigation and drought tolerance.")
        elif crop.get("water_requirement", "").lower() == "medium":
            reason_parts.append("Manageable water budget matching available irrigation.")

        reason_str = " ".join(reason_parts) or f"Compatible with {soil_clean} soil during {season_clean} season."

        recommendation_items.append(
            CropRecommendationItem(
                crop_name=c_name,
                urdu_name=u_name,
                expected_yield_maunds_per_acre=yield_str,
                estimated_gross_revenue_pkr_per_acre=gross_str,
                estimated_net_profit_pkr_per_acre=net_str,
                suitability_reason=reason_str
            )
        )

    advisory_summary = (
        f"Recommended crops for {acres} acres in {district_clean} during {season_clean} season. "
        f"Soil considered: {soil_clean.capitalize()}, Water conditions: {water_clean.capitalize()}. "
        "Grounding: Kaggle Crop Recommendation & Directorate of Agriculture Extension Punjab."
    )

    return CropPlan(
        status="success",
        district=district,
        season=season_clean,
        acres=acres,
        recommendations=recommendation_items,
        advisory_notes=advisory_summary
    )
