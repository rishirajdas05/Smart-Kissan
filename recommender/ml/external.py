import requests


def fetch_weather_openweather(city: str, api_key: str):
    """
    Returns:
      {
        city, temp_c, humidity, condition, rain_mm
      }
    If api_key missing or API fails -> returns None (caller handles fallback).
    """
    city = (city or "").strip()
    if not city or not api_key:
        return None

    try:
        # Current weather endpoint
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric"}
        r = requests.get(url, params=params, timeout=10)
        if r.status_code != 200:
            return None

        data = r.json()
        temp_c = data.get("main", {}).get("temp")
        humidity = data.get("main", {}).get("humidity")
        condition = None
        wx = data.get("weather") or []
        if wx and isinstance(wx, list):
            condition = wx[0].get("description")

        # rain: 1h or 3h
        rain_mm = 0.0
        rain = data.get("rain") or {}
        if isinstance(rain, dict):
            rain_mm = rain.get("1h") or rain.get("3h") or 0.0

        # city name from API
        api_city = data.get("name") or city

        return {
            "city": api_city,
            "temp_c": float(temp_c) if temp_c is not None else None,
            "humidity": float(humidity) if humidity is not None else None,
            "condition": condition,
            "rain_mm": float(rain_mm) if rain_mm is not None else 0.0,
        }

    except Exception:
        return None
