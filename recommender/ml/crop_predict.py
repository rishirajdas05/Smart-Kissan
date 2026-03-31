def predict_price(crop: str, month: int, year: int, city: str = "") -> float:
    crop = (crop or "").strip().lower()

    base = {
        "rice": 2400,
        "wheat": 2800,
        "maize": 2100,
        "cotton": 6200,
        "coconut": 3000,
    }.get(crop, 2500)

    # seasonality factor
    if month in [10, 11, 12]:
        base *= 1.06
    elif month in [3, 4, 5]:
        base *= 1.03

    return float(round(base, 3))
