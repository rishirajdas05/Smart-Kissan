import hashlib


_BASE_RANGES = {
    "rice": (18, 45),
    "maize": (15, 35),
    "wheat": (18, 40),
    "cotton": (55, 120),
    "coffee": (180, 320),
    "banana": (18, 40),
    "mango": (40, 140),
    "apple": (80, 220),
    "orange": (40, 120),
    "grapes": (50, 160),
    "watermelon": (12, 35),
    "papaya": (18, 60),
    "pomegranate": (80, 220),
}


def _stable_rand(seed: str) -> float:
    h = hashlib.md5(seed.encode("utf-8")).hexdigest()
    return int(h[:8], 16) / 0xFFFFFFFF


def predict_price(crop: str, city: str | None = None) -> dict:
    crop = (crop or "").lower().strip()
    city = (city or "").strip().lower()

    lo, hi = _BASE_RANGES.get(crop, (20, 120))
    r = _stable_rand(crop + "|" + city)

    price = lo + (hi - lo) * r
    trend = "up" if r > 0.62 else "down" if r < 0.38 else "stable"

    # 7-day forecast (fake but consistent)
    forecast = []
    cur = price
    for i in range(7):
        step = (r - 0.5) * 2.0  # -1..+1
        cur = max(1.0, cur + step * (0.5 + i * 0.15))
        forecast.append(round(cur, 2))

    return {
        "crop": crop,
        "city": city.title() if city else "India",
        "price_per_kg": round(price, 2),
        "trend": trend,
        "forecast_7d": forecast,
        "note": "Demo prediction (connect mandi/API later).",
    }
