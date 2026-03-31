from __future__ import annotations

import os
import math
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

# Optional: only used if you set OPENWEATHER_API_KEY
try:
    import requests  # type: ignore
except Exception:
    requests = None


@dataclass
class CropMeta:
    name: str
    season: str
    soil: str
    water: str
    fertilizer: str
    tips: str


# A bigger list so "Crops" page shows many items (not only 3)
CROPS: List[CropMeta] = [
    CropMeta("Rice", "Kharif", "Clay / loamy, water-retentive", "High", "N-rich + Zinc", "Keep field flooded early; watch pests."),
    CropMeta("Wheat", "Rabi", "Well-drained loam", "Medium", "Balanced NPK", "Avoid waterlogging; timely irrigation at tillering."),
    CropMeta("Maize", "Kharif", "Loam, well-drained", "Medium", "N-rich + Potash", "Maintain spacing; weed control early."),
    CropMeta("Cotton", "Kharif", "Black soil / well-drained", "Medium", "Potash + N", "Avoid excess nitrogen; pest monitoring."),
    CropMeta("Sugarcane", "Annual", "Deep loamy soil", "High", "NPK + organic manure", "Ensure drainage; ratoon management."),
    CropMeta("Groundnut", "Kharif", "Sandy loam", "Low-Med", "Gypsum + P", "Avoid waterlogging; calcium helps pods."),
    CropMeta("Soybean", "Kharif", "Well-drained loam", "Medium", "P + K", "Seed treatment helps; avoid late sowing."),
    CropMeta("Mustard", "Rabi", "Loam, well-drained", "Low", "N + S", "Avoid frost stress; timely irrigation."),
    CropMeta("Potato", "Rabi", "Sandy loam", "Medium", "K-rich", "Earthing up; avoid over-irrigation."),
    CropMeta("Tomato", "All season", "Loam, organic-rich", "Medium", "Balanced + micronutrients", "Stake plants; prevent fungal disease."),
    CropMeta("Onion", "Rabi", "Sandy loam", "Low-Med", "N + K", "Avoid heavy watering near harvest."),
    CropMeta("Chickpea", "Rabi", "Well-drained loam", "Low", "P-rich", "Needs less irrigation; good rotation crop."),
    CropMeta("Pigeon Pea", "Kharif", "Loam, well-drained", "Low", "P + K", "Drought tolerant; intercropping works."),
    CropMeta("Jute", "Kharif", "Alluvial, well-drained", "High", "N-rich", "Needs good moisture; timely retting."),
    CropMeta("Tea", "Perennial", "Acidic, organic-rich", "High", "N + organic", "Shade & pruning important."),
    CropMeta("Coffee", "Perennial", "Well-drained, organic", "Medium", "Balanced + organic", "Shade regulation; pest watch."),
    CropMeta("Bajra (Pearl Millet)", "Kharif", "Sandy loam", "Low", "Low inputs", "Drought tolerant; good for dry regions."),
    CropMeta("Sorghum (Jowar)", "Kharif", "Loam", "Low", "Balanced N", "Drought tolerant; avoid waterlogging."),
    CropMeta("Barley", "Rabi", "Loam, well-drained", "Low", "Moderate N", "Hardy crop; less irrigation needed."),
    CropMeta("Sunflower", "Kharif/Rabi", "Well-drained loam", "Low-Med", "P + K", "Avoid standing water; spacing matters."),
]

CROP_INDEX: Dict[str, CropMeta] = {c.name.lower(): c for c in CROPS}


def get_all_crops() -> List[CropMeta]:
    return CROPS[:]


def get_crop_meta(name: str) -> Optional[CropMeta]:
    if not name:
        return None
    return CROP_INDEX.get(name.strip().lower())


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def _normalize(value: float, lo: float, hi: float) -> float:
    if hi == lo:
        return 0.0
    return max(0.0, min(1.0, (value - lo) / (hi - lo)))


def recommend_top_crops(
    *,
    N: float,
    P: float,
    K: float,
    temperature: float,
    humidity: float,
    ph: float,
    rainfall: float,
    top_k: int = 3,
) -> List[Dict]:
    """
    Safe demo recommender:
    - If you have a real ML model, plug it here later.
    - For now, returns consistent, non-crashing results with scores + tips.
    """
    # Heuristic scoring (stable, not random)
    temp_n = _normalize(temperature, 0, 45)
    hum_n = _normalize(humidity, 0, 100)
    rain_n = _normalize(rainfall, 0, 300)
    ph_n = 1.0 - abs(ph - 6.8) / 6.8  # best around ~6.8

    fert_n = _normalize(N + P + K, 0, 400)

    base = 0.35 * temp_n + 0.25 * hum_n + 0.20 * rain_n + 0.10 * ph_n + 0.10 * fert_n
    base = max(0.0, min(1.0, base))

    # Assign crops slightly differently by season/needs
    scored: List[Tuple[CropMeta, float]] = []
    for c in CROPS:
        season_boost = 0.0
        if c.season.lower() == "kharif":
            season_boost = 0.10 * rain_n + 0.05 * hum_n
        elif c.season.lower() == "rabi":
            season_boost = 0.05 * (1.0 - rain_n) + 0.05 * (1.0 - hum_n)
        else:
            season_boost = 0.03

        score = _sigmoid(3.0 * (base + season_boost - 0.5))
        scored.append((c, float(score)))

    scored.sort(key=lambda x: x[1], reverse=True)
    out = []
    for c, s in scored[: max(1, top_k)]:
        out.append(
            {
                "name": c.name,
                "score": round(s, 2),
                "meta": {
                    "season": c.season,
                    "soil": c.soil,
                    "water": c.water,
                    "fertilizer": c.fertilizer,
                    "tips": c.tips,
                },
            }
        )
    return out


def estimate_price_demo(crop: str, city: str, qty_kg: float) -> Dict:
    """
    Demo pricing (replace later with real mandi API).
    """
    crop_key = (crop or "").strip().lower()
    city_key = (city or "").strip().lower()

    base_prices = {
        "rice": 32,
        "wheat": 28,
        "maize": 24,
        "cotton": 60,
        "sugarcane": 4,
        "groundnut": 55,
        "soybean": 48,
        "mustard": 52,
        "potato": 18,
        "tomato": 22,
        "onion": 20,
        "chickpea": 65,
        "sunflower": 58,
    }

    base = base_prices.get(crop_key, 35)

    # City factor (demo)
    factor = 1.0
    if city_key:
        if any(x in city_key for x in ["delhi", "mumbai", "bengaluru", "bangalore", "pune", "hyderabad", "chennai"]):
            factor = 1.08
        elif any(x in city_key for x in ["jaipur", "lucknow", "bhopal", "indore", "patna", "nagpur"]):
            factor = 1.04
        else:
            factor = 1.00

    qty_kg = max(0.0, float(qty_kg))
    rate = round(base * factor, 2)
    total = round(rate * qty_kg, 2)

    return {
        "crop": crop.strip() if crop else "Unknown",
        "city": city.strip() if city else "—",
        "rate_per_kg": rate,
        "quantity_kg": qty_kg,
        "total": total,
        "note": "Demo estimate (replace with real mandi rates later).",
    }


def _dummy_weather() -> Dict:
    return {
        "city": "Your Area",
        "temp_c": 15.95,
        "humidity": 62,
        "rain_mm": 12.0,
        "desc": "Partly cloudy (demo)",
    }


def get_weather_by_city(city: str) -> Dict:
    """
    Uses OpenWeatherMap if OPENWEATHER_API_KEY is set,
    otherwise returns demo weather to keep project working.
    """
    city = (city or "").strip()
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()

    if not city:
        return _dummy_weather()

    if not api_key or requests is None:
        w = _dummy_weather()
        w["city"] = city.title()
        return w

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric"}
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()

        temp_c = float(data["main"]["temp"])
        humidity = int(data["main"]["humidity"])
        rain_mm = 0.0
        if isinstance(data.get("rain"), dict):
            rain_mm = float(data["rain"].get("1h", 0.0) or 0.0)

        desc = ""
        if data.get("weather") and isinstance(data["weather"], list):
            desc = data["weather"][0].get("description", "")

        return {
            "city": data.get("name", city.title()),
            "temp_c": round(temp_c, 2),
            "humidity": humidity,
            "rain_mm": round(rain_mm, 2),
            "desc": desc or "—",
        }
    except Exception:
        w = _dummy_weather()
        w["city"] = city.title()
        w["desc"] = "Weather fetch failed (demo values used)"
        return w


def get_city_soil_defaults(city: str) -> Dict:
    """
    Since you want ONLY city in Auto page:
    We generate reasonable demo soil defaults for NPK + pH.
    Replace later with real soil datasets/APIs.
    """
    c = (city or "").strip().lower()
    # default
    N, P, K, ph = 90.0, 40.0, 40.0, 6.8

    if any(x in c for x in ["rajasthan", "jaipur", "jodhpur"]):
        N, P, K, ph = 60.0, 30.0, 35.0, 7.6
    elif any(x in c for x in ["assam", "guwahati", "meghalaya"]):
        N, P, K, ph = 95.0, 45.0, 50.0, 5.8
    elif any(x in c for x in ["punjab", "ludhiana", "amritsar"]):
        N, P, K, ph = 110.0, 50.0, 55.0, 7.2
    elif any(x in c for x in ["bihar", "patna"]):
        N, P, K, ph = 100.0, 45.0, 45.0, 6.6

    return {"N": N, "P": P, "K": K, "ph": ph}
