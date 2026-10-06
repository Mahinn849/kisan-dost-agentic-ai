from pathlib import Path
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Base project paths
BACKEND_DIR = Path(__file__).resolve().parent
BASE_DIR = BACKEND_DIR.parent
DATA_DIR = BACKEND_DIR / "data"

# Dataset paths
CROP_RECOMMENDATION_PATH = DATA_DIR / "crop_recommendation.json"
PLANT_DISEASES_PATH = DATA_DIR / "plant_diseases.json"
CROP_ECONOMICS_PATH = DATA_DIR / "crop_economics.json"
PUNJAB_SCHEMES_PATH = DATA_DIR / "punjab_govt_schemes.json"

# API & Web Scraping endpoints
AMIS_BASE_URL = "http://www.amis.pk"
OPEN_METEO_GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
AGRI_PUNJAB_URL = "https://www.agripunjab.gov.pk/"

# HTTP client settings
REQUEST_TIMEOUT_SECONDS = 15
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) KisanDost/1.0"

# OpenAI Agents SDK settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_MODEL = os.getenv("KISAN_DOST_MODEL", "gpt-4o-mini")
DB_PATH = str(BASE_DIR / "conversation.db")
