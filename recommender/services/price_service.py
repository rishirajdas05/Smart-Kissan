from __future__ import annotations
from typing import Dict
import math
import random

# Base demo prices (₹/quintal). Extend later.
BASE = {
    "rice": 2200, "maize": 1800, "cotton": 6200, "wheat": 2400,
    "banana": 1400, "mango": 3500, "apple": 8000, "coffee": 9000,
    "jute": 5200, "lentil": 6000, "chickpea": 5600,
}

def predict_price(crop: str, city: str = "") -> Dict:
    crop_key = (crop or "").strip().lower()
    base = BASE.get(crop_key, 2500)

    # deterministic-ish variation by city string
    seed = sum(ord(c) for c in (city or "")) + sum(ord(c) for c in crop_key)
    rnd = random.Random(seed)

    today = base * (0.95 + rnd.random() * 0.10)
    week = []
    for d in range(1, 8):
        # smooth wave + randomness
        factor = 1 + 0.02 * math.sin(d / 2) + (rnd.random() - 0.5) * 0.02
        week.append(round(today * factor, 2))

    return {
        "crop": crop_key,
        "city": city,
        "today": round(today, 2),
        "week": week,
        "unit": "₹ / quintal",
        "note": "Demo forecast (replace with real API/model later)."
    }
