from typing import Dict, Any
from backend.models.fertilizer_models import FertilizerPlan

# Recommended N-P-K (kg per acre) from Punjab Agriculture Directorate of Soil Fertility
CROP_NPK_REQUIREMENTS: Dict[str, Dict[str, Any]] = {
    "wheat": {
        "name": "Wheat (گندم)",
        "N_kg": 50.0,
        "P_kg": 35.0,
        "K_kg": 20.0,
        "schedule": "Apply full DAP and 1/3 Urea at sowing (Rauni/first ploughing). Apply remaining Urea in two splits at 1st irrigation (crown root) and boot stage.",
        "notes": "Do not delay phosphorus application. Broadcast Urea before irrigation or apply in standing water."
    },
    "cotton": {
        "name": "Cotton (کپاس / پھٹی)",
        "N_kg": 60.0,
        "P_kg": 30.0,
        "K_kg": 25.0,
        "schedule": "All DAP at land preparation. Apply Urea in 3 equal splits: 30-35 days after sowing, flowering initiation, and peak boll development.",
        "notes": "Excessive early nitrogen promotes vegetative rank growth. Supplement with 2% Potassium Nitrate foliar spray during boll filling."
    },
    "rice": {
        "name": "Rice (چاول)",
        "N_kg": 55.0,
        "P_kg": 35.0,
        "K_kg": 20.0,
        "schedule": "All DAP at puddle transplanting. Urea in two equal splits: 25-30 days and 45-50 days after transplanting.",
        "notes": "Add 5 kg Zinc Sulphate (33%) at 30 days after transplanting to prevent Khaira (Hadda) disease."
    },
    "maize": {
        "name": "Maize (مکئی)",
        "N_kg": 75.0,
        "P_kg": 45.0,
        "K_kg": 30.0,
        "schedule": "All DAP + 1/3 Urea at sowing. Split remaining Urea at knee-high stage and before tasseling.",
        "notes": "Hybrid maize is a heavy feeder. Ensure balanced potash to prevent stalk lodging."
    },
    "sugarcane": {
        "name": "Sugarcane (کماد / گنا)",
        "N_kg": 85.0,
        "P_kg": 45.0,
        "K_kg": 40.0,
        "schedule": "Full DAP at planting in furrows. Split Urea across 3 irrigations by the end of June before earthing up.",
        "notes": "Do not apply nitrogen past July as it reduces cane sucrose brix and delays maturity."
    },
    "potato": {
        "name": "Potato (آلو)",
        "N_kg": 80.0,
        "P_kg": 50.0,
        "K_kg": 50.0,
        "schedule": "All DAP and SOP at ridge making/planting. Split Urea at first earthing-up and tuber initiation.",
        "notes": "SOP (Sulphate of Potash) is preferred over MOP to ensure solid dry matter in tubers."
    },
    "gram": {
        "name": "Gram / Chickpea (چنا)",
        "N_kg": 15.0,
        "P_kg": 25.0,
        "K_kg": 10.0,
        "schedule": "Apply starter DAP at sowing. Legume root nodules fix biological atmospheric nitrogen naturally.",
        "notes": "Avoid excess nitrogen, which halts flower setting and stimulates vegetative foliage."
    },
    "mustard": {
        "name": "Mustard / Raya (سرسوں)",
        "N_kg": 35.0,
        "P_kg": 25.0,
        "K_kg": 15.0,
        "schedule": "Full DAP and half Urea at sowing; remaining Urea at first irrigation after thinning.",
        "notes": "Sulphur application (Gypsum or elemental S) enhances seed oil content significantly."
    }
}

# Standard benchmark fertilizer prices in Pakistan (PKR per 50 kg bag)
UREA_BAG_PRICE_PKR = 5000
DAP_BAG_PRICE_PKR = 13000
SOP_BAG_PRICE_PKR = 14500

def compute_fertilizer_plan(crop: str, acres: float) -> FertilizerPlan:
    """
    Computes exact per-acre NPK requirement and converts into bags of Urea, DAP,
    and total investment in PKR based on verified agronomic nutrient ratios.
    """
    crop_clean = crop.lower().strip()

    matched_key = None
    for key in CROP_NPK_REQUIREMENTS:
        if key in crop_clean or crop_clean in key:
            matched_key = key
            break

    if not matched_key:
        # Default generalized agronomic profile
        cfg = {
            "name": crop.capitalize(),
            "N_kg": 50.0,
            "P_kg": 30.0,
            "K_kg": 20.0,
            "schedule": "Apply full DAP at sowing and split Urea during vegetative irrigations.",
            "notes": "Standard baseline recommendation. Conduct soil test (Soil Fertility Lab) for precision dosing."
        }
    else:
        cfg = CROP_NPK_REQUIREMENTS[matched_key]

    n_per_acre = cfg["N_kg"]
    p_per_acre = cfg["P_kg"]
    k_per_acre = cfg["K_kg"]

    # Nutrient calculations:
    # 1 bag DAP (50kg) = 23 kg P2O5 and 9 kg N
    # 1 bag Urea (50kg) = 23 kg N
    dap_bags_per_acre = round(p_per_acre / 23.0, 2)
    n_from_dap_per_acre = dap_bags_per_acre * 9.0
    remaining_n_per_acre = max(0.0, n_per_acre - n_from_dap_per_acre)
    urea_bags_per_acre = round(remaining_n_per_acre / 23.0, 2)

    total_dap_bags = round(dap_bags_per_acre * acres, 1)
    total_urea_bags = round(urea_bags_per_acre * acres, 1)

    total_n_kg = round(n_per_acre * acres, 1)
    total_p_kg = round(p_per_acre * acres, 1)
    total_k_kg = round(k_per_acre * acres, 1)

    urea_cost = int(round(total_urea_bags * UREA_BAG_PRICE_PKR))
    dap_cost = int(round(total_dap_bags * DAP_BAG_PRICE_PKR))
    total_cost = urea_cost + dap_cost

    return FertilizerPlan(
        status="success",
        crop=cfg["name"],
        acres=acres,
        nitrogen_req_kg=total_n_kg,
        phosphorus_req_kg=total_p_kg,
        potassium_req_kg=total_k_kg,
        urea_bags=total_urea_bags,
        dap_bags=total_dap_bags,
        sop_bags=0.0,
        urea_cost_pkr=urea_cost,
        dap_cost_pkr=dap_cost,
        total_cost_pkr=total_cost,
        application_schedule=cfg["schedule"],
        notes=cfg["notes"]
    )
