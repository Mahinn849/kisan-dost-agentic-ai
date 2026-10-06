# 🌾 Kisan Dost (کسان دوست) — Advanced Agronomy AI Platform
### Built natively with OpenAI Agents SDK • Terminal Agent Challenge & Web Interface

**Kisan Dost ("Farmer's Friend")** is a production-grade, multi-agent agritech advisory system designed specifically for smallholder farmers and field extension officers across Pakistan. It provides a 24/7 intelligent helpline that translates plain Urdu, English, and Roman Urdu queries into actionable, scientifically verified agronomic guidance, live market rates, weather alerts, and financial budgets.

---

## 🎯 The Problem Worth Solving
Agriculture forms the backbone of Pakistan's economy, yet smallholder farmers often make high-stakes, season-defining decisions—what to plant, how much fertilizer to buy, how to cure pest infestations, when and where to sell—with almost no immediate agronomic support. One government extension officer is frequently responsible for thousands of farming families. Kisan Dost bridges this critical gap with an agentic, data-driven AI assistant that delivers accurate, grounded answers in seconds.

---

## 🏗️ Agentic Architecture (OpenAI Agents SDK)

Kisan Dost is architected around a supervisor triage router with bidirectional handoffs to five specialist nodes:

```text
                                  🧑‍🌾 Pakistani Farmer
                                           │
                                           ▼
                            ┌─────────────────────────────┐
                            │      Input Guardrail        │
                            │ (Agri vs Off-Topic / Crypto)│
                            └──────────────┬──────────────┘
                                           │
                                           ▼
                            ┌─────────────────────────────┐
                            │     Triage Agent Router     │
                            │       ("Kisan Dost")        │
                            └──────┬───────┬───────┬──────┘
                                   │       │       │
            ┌──────────────────────┘       │       └──────────────────────┐
            ▼                              ▼                              ▼
  ┌───────────────────┐          ┌───────────────────┐          ┌───────────────────┐
  │  Agronomy Agent   │          │ Pest Doctor Agent │          │   Market Agent    │
  ├───────────────────┤          ├───────────────────┤          ├───────────────────┤
  │ • crop_advisor    │          │ • pest_disease_   │          │ • mandi_price_    │
  │ • fertilizer_calc │          │   doctor          │          │   lookup          │
  └─────────┬─────────┘          └─────────┬─────────┘          │ • govt_support_   │
            │                              │                    │   finder          │
            │                              │                    └─────────┬─────────┘
            ▼                              ▼                              │
  ┌───────────────────┐          ┌───────────────────┐                    │
  │   Finance Agent   │          │   Weather Agent   │                    │
  ├───────────────────┤          ├───────────────────┤                    │
  │ • profit_estimator│          │ • irrigation_     │                    │
  │   (PBS Benchmarks)│          │   weather (Meteo) │                    │
  └───────────────────┘          └───────────────────┘                    │
                                           │                              │
                                           ▼                              ▼
                            ┌─────────────────────────────┐
                            │      Output Guardrail       │
                            │(Pesticide & Medical Safety) │
                            └──────────────┬──────────────┘
                                           │
                                           ▼
                                 🌾 Farmer Advisory
```

### Specialist Agent Network:
1. **Triage Agent (`Kisan Dost`)**: Front-line conversational greeter and router. Assesses intent, captures farmer profile context, and executes multi-agent handoffs.
2. **Agronomy Agent**: Recommends optimal crops tailored to soil, season, and irrigation, and calculates precise NPK fertilizer requirements in bags of Urea and DAP.
3. **Pest Doctor Agent**: Identifies crop diseases and insect pests from leaf symptoms; enforces strict pesticide dosage safety limits.
4. **Market Agent**: Scrapes live wholesale market rates from AMIS Punjab and matches provincial support schemes (Kisan Card).
5. **Finance Agent**: Generates complete full-season farm budgets, net margin projections, and break-even yield thresholds.
6. **Weather Agent**: Interprets live Open-Meteo meteorological telemetry for Pakistani districts and provides stage-based irrigation advice and frost/heat hazard warnings.

---

## 🛠️ Complete 7-Tool Matrix & Data Grounding

Every capability is implemented as a typed `@function_tool` returning validated Pydantic models with explicit status tracking:

| # | Tool Name | Specialist Agent | Data Stream Type | Grounded Data Source & URL | Output Schema |
|---|---|---|---|---|---|
| 1 | `crop_advisor` | Agronomy Agent | Dataset & Agro-Climatic Matrix | [Kaggle Crop Recommendation](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset) & Directorate of Agriculture Extension Punjab | `CropPlan` |
| 2 | `fertilizer_calculator` | Agronomy Agent | Calculated Agronomic Algorithm | Punjab Soil Fertility Labs (NPK conversions to Urea 46% N & DAP 18-46-0) | `FertilizerPlan` |
| 3 | `pest_disease_doctor` | Pest Doctor Agent | Grounded Knowledge & IPM Rules | [PlantVillage Leaf Disease Dataset](https://github.com/spMohanty/PlantVillage-Dataset) & Agri Extension Punjab Pest Warning | `PestDiagnosis` |
| 4 | `mandi_price_lookup` | Market Agent | **Live Web Scraper** (HTTP) | **AMIS Punjab Daily Mandi Rates** (`http://www.amis.pk/`) *(136 commodities)* | `MandiPriceResult` |
| 5 | `irrigation_weather` | Weather Agent | **Live REST APIs** | [Open-Meteo Geocoding](https://geocoding-api.open-meteo.com/) & [Open-Meteo Weather](https://open-meteo.com/) | `WeatherResult` |
| 6 | `profit_estimator` | Finance Agent | Calculated & Official Benchmarks | [Pakistan Bureau of Statistics (PBS)](https://www.pbs.gov.pk/) & [FAOSTAT Pakistan](https://www.fao.org/faostat/en/#country/165) | `ProfitEstimate` |
| 7 | `govt_support_finder` | Market Agent | Grounded Policy Directory | [Agriculture Department, Punjab](https://www.agripunjab.gov.pk/) (CM Kisan Card, Subsidies) | `GovtSupportResult` |

---

## 🛡️ Dual-Layer Safety Guardrails

### 1. Input Guardrail (`agriculture_input_guardrail`)
- Pre-execution check verifying that incoming user prompts are strictly related to farming, crops, livestock, fertilizers, weather, or agriculture.
- Quick-pass optimization for common agricultural vocabulary to guarantee near-zero latency.
- Off-topic prompts (crypto, stock trading, politics, hacking, human medicine) actively trip the guardrail wire (`InputGuardrailTripwireTriggered`), gracefully alerting the user.

### 2. Output Guardrail (`pesticide_safety_guardrail`)
- Intercepts generated advice before reaching the farmer.
- **Pesticide Safety Check**: Blocks dangerous or banned agricultural chemicals (DDT, Aldrin, Paraquat). Enforces that unverified chemicals never receive guessed dosages (enforcing `dosage_unavailable`).
- **Human Medical Block**: Blocks pharmaceutical prescriptions, painkillers (Panadol, Brufen), or human medical advice.

---

## 📊 Truthful Data & Real Fallback Policy

Kisan Dost enforces strict truthfulness across all external integrations:

- **AMIS Mandi Prices**:
  - The AMIS tool connects via HTTP (`http://www.amis.pk/`) to scrape real-time wholesale tables.
  - If a commodity was not traded today in a specific market (e.g. Wheat in Lahore returning `-`), the tool **never invents a fake price**. It reports `price_not_available` and states honestly that no wholesale trades were posted today.
  - If an unsupported crop is requested, it returns `unsupported_crop`.
- **Live Weather**:
  - Connects live to Open-Meteo. If the geocoding API cannot resolve a location, it returns `location_not_found`.
  - If network fails, it returns `source_unavailable` or `timeout`. It never generates fake temperatures.
- **Safe Dosages**:
  - If a crop disease symptom is ambiguous or unverified, `safe_dosage` returns `"dosage_unavailable"` and warns the farmer to physically verify with the local extension office.

---

## 💾 Sessions & Persistent Context Memory

- **`SQLiteSession`**: Conversation history is persisted in `conversation.db` using the Agents SDK session storage.
- **`FarmerProfile` Typed Context**: Captures the farmer's district (e.g. Multan), acreage (e.g. 5 acres), soil type, and current crop across turns. The farmer does not need to re-type basic parameters on every message.

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Internet access (for live AMIS Punjab scraping and Open-Meteo weather API)

### 1. Clone & Set Up Environment
```bash
# Clone the repository
git clone https://github.com/your-username/HACKATHON-KISAN-DOST.git
cd HACKATHON-KISAN-DOST

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and set your OpenAI API key:
```bash
cp .env.example .env
```
In `.env`:
```env
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
# Optional model override (defaults to gpt-4o-mini)
# KISAN_DOST_MODEL=gpt-4o-mini
```
*Note: Any OpenAI-compatible provider (Gemini, Groq) can also be used by setting `OPENAI_BASE_URL`.*

---

## 💻 Running Kisan Dost

### Option A: Terminal Agent Challenge (Core Rubric Deliverable)
```bash
python run_cli.py
```
*Launches the interactive terminal advisory loop with colored status headers, active agent tracking, and graceful exit (`exit`, `quit`, `q`).*

### Option B: Web Dashboard (Bonus Full-Stack Interface)
```bash
python run_web.py
```
*Launches the modern web dashboard interface at `http://127.0.0.1:8000` with the `/api/chat` agentic bridge.*

### Option C: Unified Runner
```bash
python kisan_dost.py          # Starts Terminal Agent CLI by default
python kisan_dost.py --web    # Starts FastAPI Web Dashboard
```

---

## 🧪 Automated Testing Suite

Kisan Dost includes a complete test suite covering all 7 tools, edge cases, fallbacks, and guardrails:

```bash
pytest tests/ -v
```

### Test Coverage:
- `test_mandi.py`: Live AMIS Rice rates in Lahore, unsupported crop refusal, district not found, and unquoted commodity truthful handling.
- `test_weather.py`: Live Open-Meteo weather in Multan, location not found, and growth stage advisories.
- `test_pest_doctor.py`: Cotton whitefly diagnosis with safe dosage, wheat rust, unknown symptom dosage refusal (`dosage_unavailable`), and unsupported crop safety.
- `test_crop_advisor.py`: Rabi season crop selection in Multan, Kharif season canal rice selection, and invalid season handling.
- `test_fertilizer.py`: Wheat 5-acre NPK to Urea/DAP bag computation, negative acreage normalization, and uncommon crop fallbacks.
- `test_profit.py`: PBS benchmark crop budget evaluation and custom farmer cost input evaluation.
- `test_support.py`: CM Punjab Kisan Card retrieval (PKR 150,000 credit, 8070 SMS), solar tubewell subsidy, and non-Punjab queries.
- `test_guardrails.py`: Human medicine blocking (Panadol), banned chemical blocking (DDT), safe agronomy advice pass-through, and agricultural input quick-pass.

**Result: 26 passed out of 26 tests (100% pass rate).**

---

## 🌾 Example Farmer Inquiries

1. **Composite Planning (The Hackathon Demo Moment)**:
   > *"A farmer in Multan asks what to plant this Rabi season on 5 acres with limited water. Also calculate the fertilizer plan, whitefly treatment, and what government subsidy to apply for."*
2. **Live Mandi Rates**:
   > *"Faisalabad aur Lahore mein rice aur wheat ka taza mandi rate kya hai?"*
3. **Pest Identification & Safety**:
   > *"Cotton leaves are curling and I can see tiny white insects on the undersides. What is the safe spray dosage?"*
4. **Extreme Weather & Irrigation**:
   > *"Multan mein wheat flowering stage par hai, kya kal paani lagana chahiye aur koi shadeed mausam ka khatra to nahi?"*
5. **Full Season Budget & Profit**:
   > *"5 acres gandum lagane par total kharcha kitna aayega aur estimated net profit kitna hoga?"*
6. **Govt Kisan Card**:
   > *"Punjab mein Kisan Card ke zariye fertilizer par subsidy ya loan lene ka kya tareeqa hai?"*

---

## 📁 Clean Full-Stack Directory Structure (Frontend & Backend)

```text
HACKATHON KISAN DOST/
│
├── frontend/                           # FRONTEND UI & PRESENTATION LAYER
│   └── templates/
│       └── index.html                  # Professional White Agritech Dashboard UI
│
├── backend/                            # BACKEND AGENTIC AI & API CORE
│   ├── __init__.py
│   ├── config.py                       # App settings, timeouts, endpoints, paths
│   ├── api.py                          # FastAPI chat & web server application
│   │
│   ├── agents/                         # OpenAI Agents SDK multi-agent network
│   │   ├── __init__.py
│   │   ├── triage_agent.py             # Main Kisan Dost supervisor router
│   │   ├── agronomy_agent.py           # Crop Advisor & Fertilizer Specialist
│   │   ├── pest_doctor_agent.py        # Pest & Disease Doctor
│   │   ├── market_agent.py             # AMIS Mandi prices & Govt support
│   │   ├── finance_agent.py            # Budget & Profit Estimator
│   │   └── weather_agent.py            # Meteorology & Irrigation Advisor
│   │
│   ├── tools/                          # Typed @function_tool implementations
│   │   ├── __init__.py
│   │   ├── crop_advisor.py
│   │   ├── pest_disease_doctor.py
│   │   ├── fertilizer_calculator.py
│   │   ├── mandi_price_lookup.py
│   │   ├── irrigation_weather.py
│   │   ├── profit_estimator.py
│   │   └── govt_support_finder.py
│   │
│   ├── models/                         # Validated Pydantic output schemas
│   │   ├── __init__.py
│   │   ├── context_models.py           # FarmerProfile typed session context
│   │   ├── crop_models.py              # CropPlan, CropRecommendationItem
│   │   ├── pest_models.py              # PestDiagnosis
│   │   ├── fertilizer_models.py        # FertilizerPlan (NPK, Urea, DAP bags)
│   │   ├── mandi_models.py             # MandiPriceResult (AMIS live rates)
│   │   ├── weather_models.py           # WeatherResult (Open-Meteo telemetry)
│   │   ├── profit_models.py            # ProfitEstimate, CostBreakdown
│   │   └── support_models.py           # GovtSupportResult, SchemeDetail
│   │
│   ├── services/                       # Data services & live scrapers
│   │   ├── __init__.py
│   │   ├── amis_mandi_service.py       # Live AMIS HTTP scraper (136 commodities)
│   │   ├── open_meteo_service.py       # Live geocoding & weather forecast client
│   │   ├── crop_dataset_service.py     # Grounded Kaggle Crop Recommendation matcher
│   │   ├── plant_village_service.py    # PlantVillage & Agri Punjab disease doctor
│   │   ├── fertilizer_service.py       # NPK nutrient conversion engine
│   │   ├── benchmark_cost_service.py   # PBS / FAOSTAT crop production economics
│   │   └── punjab_agri_service.py      # Verified Punjab Agri Department schemes
│   │
│   ├── guardrails/                     # Active Agents SDK guardrails
│   │   ├── __init__.py
│   │   ├── input_guardrail.py          # Topic inspector with active tripwire
│   │   └── pesticide_safety.py         # Chemical and human medicine blocker
│   │
│   └── data/                           # Grounded datasets
│       ├── crop_recommendation.json    # Grounded Kaggle crop data & Punjab zones
│       ├── plant_diseases.json         # PlantVillage & Agri Punjab disease library
│       ├── crop_economics.json         # PBS & FAOSTAT benchmark production costs
│       └── punjab_govt_schemes.json    # Official Punjab schemes & Kisan Card details
│
├── tests/                              # Automated Pytest suite (26/26 tests passing)
│   ├── __init__.py
│   ├── test_crop_advisor.py
│   ├── test_pest_doctor.py
│   ├── test_fertilizer.py
│   ├── test_mandi.py
│   ├── test_weather.py
│   ├── test_profit.py
│   ├── test_support.py
│   └── test_guardrails.py
│
├── run_cli.py                          # Primary Terminal Agent entrypoint (Rubric Core)
├── run_web.py                          # Bonus FastAPI Web server entrypoint
├── kisan_dost.py                       # Unified entrypoint (CLI default / --web)
├── requirements.txt                    # Pinned Python dependencies
├── .env.example                        # Template for environment variables
├── .gitignore                          # Clean git exclusions (.env, DB, caches)
└── README.md                           # Comprehensive documentation
```

---

## 📌 Limitations & Future Enhancements
1. **Sindh & KP Mandi Integration**: AMIS Punjab currently covers wholesale markets in Punjab province. Expanding to Sindh Agriculture Marketing Department is planned.
2. **Computer Vision Leaf Scan**: Adding direct smartphone camera photo analysis for leaf spots using deep learning (CNNs trained on PlantVillage).
3. **Interactive Voice (Urdu / Punjabi)**: Integrating whisper-based voice in/out for illiterate smallholder farmers.

---

*Developed under strict specifications compliance for the Agentic AI Hackathon (Terminal Agent Challenge).*
