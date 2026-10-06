import requests
from typing import Optional
from backend.config import (
    OPEN_METEO_GEO_URL,
    OPEN_METEO_FORECAST_URL,
    REQUEST_TIMEOUT_SECONDS,
    DEFAULT_USER_AGENT
)
from backend.models.weather_models import WeatherResult

def fetch_weather_and_irrigation_advisory(district: str, crop_stage: str) -> WeatherResult:
    """
    Fetches real-time weather metrics from Open-Meteo Geocoding & Weather API
    and provides grounded irrigation timing and extreme weather hazard advisories.
    """
    district_clean = district.strip()
    stage_clean = crop_stage.lower().strip()

    headers = {
        "User-Agent": DEFAULT_USER_AGENT
    }

    try:
        # Step 1: Geocode district
        geo_params = {
            "name": district_clean,
            "count": 1,
            "language": "en",
            "format": "json",
            "countryCode": "PK"
        }
        geo_res = requests.get(OPEN_METEO_GEO_URL, params=geo_params, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
        geo_res.raise_for_status()
        geo_data = geo_res.json()

        results = geo_data.get("results", [])
        if not results:
            return WeatherResult(
                status="location_not_found",
                district=district,
                resolved_location=district,
                crop_stage=crop_stage,
                irrigation_advisory="Weather location could not be confirmed. Maintain standard regional watering.",
                hazard_warning="No weather hazards could be determined for unverified location.",
                message=f"Could not find Pakistani location '{district}'. Please provide a recognized city or district."
            )

        loc = results[0]
        lat = loc["latitude"]
        lon = loc["longitude"]
        resolved_name = loc.get("name", district)

        # Step 2: Fetch weather forecast
        forecast_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto",
            "forecast_days": 3
        }
        weather_res = requests.get(OPEN_METEO_FORECAST_URL, params=forecast_params, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
        weather_res.raise_for_status()
        w_data = weather_res.json()

        current = w_data.get("current", {})
        daily = w_data.get("daily", {})

        current_temp = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")

        max_temps = daily.get("temperature_2m_max", [None])
        min_temps = daily.get("temperature_2m_min", [None])
        rains = daily.get("precipitation_sum", [0.0])

        max_temp = max_temps[0] if max_temps else None
        min_temp = min_temps[0] if min_temps else None
        rain_today = rains[0] if rains else 0.0

        # Step 3: Hazard detection
        frost_alert = False
        heatwave_alert = False
        hazard_parts = []

        if min_temp is not None and min_temp < 4.0:
            frost_alert = True
            hazard_parts.append(f"⚠️ FROST RISK: Minimum temperature forecasted at {min_temp}°C (<4°C). Apply light night irrigation or smoke cover to protect sensitive crop canopy.")

        if (max_temp is not None and max_temp >= 40.0) or (current_temp is not None and current_temp >= 39.0):
            heatwave_alert = True
            hazard_parts.append(f"🔥 HEATWAVE WARNING: Temperature reaching {max_temp or current_temp}°C. Elevate soil moisture to prevent heat stress and flower shedding.")

        if rain_today is not None and rain_today >= 20.0:
            hazard_parts.append(f"🌧️ HEAVY RAINFALL WARNING: Expected {rain_today} mm rain today. Clear field drainage ditches to prevent root asphyxiation.")

        hazard_summary = " ".join(hazard_parts) if hazard_parts else "No acute weather hazards detected for the next 24 hours."

        # Step 4: Agronomic Irrigation Advisory
        if rain_today is not None and rain_today >= 5.0:
            irrigation_advice = f"Rain expected ({rain_today} mm). Suspend irrigation to avoid water wastage and root rot. Re-evaluate moisture 24h after rainfall."
        elif heatwave_alert:
            irrigation_advice = "Extreme heat detected. Irrigate during early morning or evening hours. Avoid mid-day watering to minimize thermal shock."
        elif "seedling" in stage_clean or "germination" in stage_clean:
            irrigation_advice = "Seedling stage: Maintain light, uniform moisture (Rauni). Avoid crusting or deep flooding which drowns young radicles."
        elif "vegetative" in stage_clean:
            irrigation_advice = "Vegetative stage: Ensure adequate root-zone moisture to support leaf area expansion. Irrigate at 50% field capacity depletion."
        elif "flowering" in stage_clean or "pollination" in stage_clean:
            irrigation_advice = "Flowering stage is critically water-sensitive. Moisture stress will trigger floret abortion; maintain steady, shallow irrigation."
        elif "grain" in stage_clean or "milking" in stage_clean or "dough" in stage_clean:
            irrigation_advice = "Grain filling stage: Water moderately to guarantee plump grain test weight. Do not allow soil to crack."
        elif "maturity" in stage_clean or "harvest" in stage_clean:
            irrigation_advice = "Ripening/Maturity stage: Stop irrigation 10-15 days prior to harvest to promote uniform drying and prevent crop lodging."
        else:
            irrigation_advice = "Monitor soil moisture at 6-inch depth. Proceed with standard irrigation schedule matching local canal availability."

        return WeatherResult(
            status="live",
            district=district,
            resolved_location=resolved_name,
            latitude=lat,
            longitude=lon,
            crop_stage=crop_stage,
            current_temperature_c=current_temp,
            relative_humidity_pct=humidity,
            max_temperature_c=max_temp,
            min_temperature_c=min_temp,
            expected_rain_mm=rain_today,
            frost_warning=frost_alert,
            heatwave_warning=heatwave_alert,
            irrigation_advisory=irrigation_advice,
            hazard_warning=hazard_summary,
            source="Open-Meteo Weather API",
            message=f"Live meteorological metrics successfully retrieved for {resolved_name}."
        )

    except requests.exceptions.Timeout:
        return WeatherResult(
            status="timeout",
            district=district,
            resolved_location=district,
            crop_stage=crop_stage,
            irrigation_advisory="Weather connection timed out. Maintain conservative irrigation based on physical soil moisture check.",
            hazard_warning="Weather hazard checks temporarily offline due to network timeout.",
            message="Open-Meteo API connection timed out. Live telemetry currently unavailable."
        )
    except requests.exceptions.RequestException as e:
        return WeatherResult(
            status="source_unavailable",
            district=district,
            resolved_location=district,
            crop_stage=crop_stage,
            irrigation_advisory="Live weather provider unreachable. Do not modify irrigation without manual soil inspection.",
            hazard_warning="Live weather warning system currently unreachable.",
            message=f"Failed to communicate with Open-Meteo API: {str(e)}"
        )
    except Exception as e:
        return WeatherResult(
            status="error",
            district=district,
            resolved_location=district,
            crop_stage=crop_stage,
            irrigation_advisory="Weather data processing error. Follow standard agronomic practices.",
            hazard_warning="Could not evaluate weather hazards.",
            message=f"Unexpected error in weather pipeline: {str(e)}"
        )
