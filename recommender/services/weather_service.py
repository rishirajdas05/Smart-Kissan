from __future__ import annotations
from typing import Optional, Dict
import requests

def get_weather_by_city(city: str) -> Dict[str, float]:
    """
    Returns: temperature, humidity, rainfall
    Uses Open-Meteo geocoding + forecast (no key needed).
    Fallback values if API fails.
    """
    city = (city or "").strip()
    if not city:
        return {"temperature": 25.0, "humidity": 60.0, "rainfall": 100.0}

    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=8,
        ).json()

        if not geo.get("results"):
            return {"temperature": 25.0, "humidity": 60.0, "rainfall": 100.0}

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        forecast = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m",
                "hourly": "precipitation",
            },
            timeout=8,
        ).json()

        cur = forecast.get("current", {})
        temp = float(cur.get("temperature_2m", 25.0))
        hum = float(cur.get("relative_humidity_2m", 60.0))

        # approximate rainfall: sum of last 24 hourly precipitation if present
        rainfall = 100.0
        hourly = forecast.get("hourly", {})
        precip = hourly.get("precipitation")
        if isinstance(precip, list) and len(precip) >= 24:
            rainfall = float(sum(precip[-24:]))

        return {"temperature": temp, "humidity": hum, "rainfall": rainfall}

    except Exception:
        return {"temperature": 25.0, "humidity": 60.0, "rainfall": 100.0}
