import csv
import os
from functools import lru_cache

def _price_path():
    base = os.path.dirname(__file__)
    ds_dir = os.path.abspath(os.path.join(base, "..", "dataset"))
    return os.path.join(ds_dir, "crop_prices_sample.csv")


@lru_cache(maxsize=1)
def _load_price_rows():
    path = _price_path()
    data = {}
    global_prices = []

    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            crop = (r.get("crop") or "").strip().lower()
            market = (r.get("market") or "").strip().lower()
            year = int(r.get("year"))
            month = int(r.get("month"))
            price = float(r.get("price_inr_per_quintal"))

            global_prices.append(price)
            key = (crop, market, month)
            data.setdefault(key, []).append((year, price))

    default_price = sum(global_prices) / max(1, len(global_prices))
    return data, default_price


def _linreg(points):
    # points: [(x, y)]
    n = len(points)
    if n < 2:
        return None
    sx = sum(x for x, _ in points)
    sy = sum(y for _, y in points)
    sxx = sum(x * x for x, _ in points)
    sxy = sum(x * y for x, y in points)
    den = (n * sxx - sx * sx)
    if den == 0:
        return None
    a = (n * sxy - sx * sy) / den
    b = (sy - a * sx) / n
    return a, b


def predict_price(crop: str, year: int, month: int, market: str = ""):
    data, default_price = _load_price_rows()

    crop_key = (crop or "").strip().lower()
    market_key = (market or "").strip().lower()

    # Try exact crop+market+month
    pts = data.get((crop_key, market_key, month))
    if not pts and market_key:
        # fallback: any market for this crop+month
        pts = []
        for (c, m, mo), v in data.items():
            if c == crop_key and mo == month:
                pts.extend(v)

    if not pts:
        # fallback: any month crop
        pts = []
        for (c, m, mo), v in data.items():
            if c == crop_key:
                pts.extend(v)

    if not pts:
        return round(default_price, 2)

    reg = _linreg(pts)
    if not reg:
        # avg fallback
        avg = sum(p for _, p in pts) / len(pts)
        return round(avg, 2)

    a, b = reg
    pred = a * year + b
    return round(pred, 2)
