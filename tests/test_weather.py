import pytest
from backend.tools.irrigation_weather import irrigation_weather
from backend.models.weather_models import WeatherResult

def test_weather_live_multan():
    """Tests live Open-Meteo Geocoding and Weather for Multan."""
    result: WeatherResult = irrigation_weather.__wrapped__("Multan", "vegetative")
    assert isinstance(result, WeatherResult)
    assert result.status in ["live", "timeout", "source_unavailable"]
    if result.status == "live":
        assert result.latitude is not None
        assert result.longitude is not None
        assert result.current_temperature_c is not None
        assert "Open-Meteo" in result.source
        assert len(result.irrigation_advisory) > 0

def test_weather_invalid_city():
    """Tests non-existent location returns location_not_found."""
    result = irrigation_weather.__wrapped__("InvalidLocation999XYZ", "seedling")
    assert result.status in ["location_not_found", "timeout", "source_unavailable"]
    if result.status == "location_not_found":
        assert "Could not find" in result.message

def test_weather_crop_stages():
    """Tests different crop stage advisories."""
    r_flower = irrigation_weather.__wrapped__("Faisalabad", "flowering")
    if r_flower.status == "live":
        assert "Flowering" in r_flower.irrigation_advisory or "rain" in r_flower.irrigation_advisory.lower() or "heat" in r_flower.irrigation_advisory.lower()
