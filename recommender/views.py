from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timesince import timesince

from .forms import (
    ManualRecommendationForm, AutoCityForm, PriceForm, SoilForm, FeedbackForm
)
from .crop_data import CROPS


# ---------------- SESSION HELPERS ----------------

def _bump(request, key: str):
    usage = request.session.get("usage", {})
    usage[key] = int(usage.get(key, 0)) + 1
    request.session["usage"] = usage
    request.session["last_activity"] = timezone.now().isoformat()
    request.session.modified = True


def _track_popularity(request, crop_names):
    pop = request.session.get("popularity", {})
    for c in crop_names:
        if not c:
            continue
        c = str(c)
        pop[c] = int(pop.get(c, 0)) + 1
    request.session["popularity"] = pop
    request.session.modified = True


# ---------------- IMPOSSIBLE VALUE CHECK ----------------

def _check_impossible(temp, hum, ph, rain):
    """
    Returns a list of error strings for physically impossible input values.
    These are values that cannot exist in the real world.
    """
    errors = []

    # Temperature: absolute limits for agriculture
    if temp > 50:
        errors.append(f"Temperature {temp}°C is impossible for crop growth (max 50°C).")
    if temp < -10:
        errors.append(f"Temperature {temp}°C is too extreme for any crop.")

    # Humidity: physically impossible above 100%
    if hum > 100:
        errors.append(f"Humidity {hum}% is physically impossible — maximum is 100%.")
    if hum < 0:
        errors.append(f"Humidity cannot be negative.")

    # pH: scale is 0–14, agriculture range is 3–10
    if ph > 14:
        errors.append(f"Soil pH {ph} is physically impossible — pH scale is 0–14.")
    if ph > 10:
        errors.append(f"Soil pH {ph} is extremely alkaline — no crops grow above pH 10.")
    if ph < 3:
        errors.append(f"Soil pH {ph} is extremely acidic — no crops grow below pH 3.")

    # Rainfall: extreme upper limit
    if rain > 500:
        errors.append(f"Rainfall {rain}mm is extreme flooding — no crops survive this.")

    return errors


# ---------------- IMPROVED SCORING ----------------

def _score_crop(crop, temp, hum, ph, rain):
    """
    Scoring with hard disqualification for out-of-range values.
    Impossible values are already caught before this function is called.
    """

    def hard_disqualify(val, low, high, tolerance=0.10):
        span = max(1.0, high - low)
        margin = span * tolerance
        return val < (low - margin) or val > (high + margin)

    def in_range_score(val, low, high):
        if low <= val <= high:
            return 1.0
        span = max(1.0, high - low)
        dist = min(abs(val - low), abs(val - high))
        return max(0.0, 1.0 - (dist / span))

    # === HARD DISQUALIFICATION ===
    # Temperature is most critical
    if hard_disqualify(temp, crop["temp_min"], crop["temp_max"], tolerance=0.10):
        return 0.0

    # Rainfall: only hard-disqualify if rain=0 and crop needs lots
    if rain == 0 and crop["rain_min"] > 150:
        return 0.0

    # Climate zone checks
    zone = crop.get("climate_zone", "all")
    if zone == "hill" and temp > 25:
        return 0.0
    if zone == "coastal" and hum < 40:
        return 0.0
    if zone == "arid" and rain > 250 and hum > 85:
        return 0.0

    # === SOFT SCORING ===
    s = 0
    s += in_range_score(temp, crop["temp_min"], crop["temp_max"])
    s += in_range_score(hum, crop["hum_min"], crop["hum_max"])
    s += in_range_score(ph, crop["ph_min"], crop["ph_max"])
    s += in_range_score(rain, crop["rain_min"], crop["rain_max"])

    return round((s / 4.0) * 100, 1)


# ---------------- PAGES ----------------

def home(request):
    _bump(request, "home")
    return render(request, "recommender/home.html", {"active": "home"})


def manual(request):
    _bump(request, "manual")

    from django.urls import reverse, NoReverseMatch
    try:
        crops_url = reverse("recommender:crops")
    except NoReverseMatch:
        try:
            crops_url = reverse("crops")
        except NoReverseMatch:
            crops_url = "/crops/"

    results = []
    tips = []
    searched = False
    impossible = False   # flag for physically impossible inputs
    impossible_errors = []
    form = ManualRecommendationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        searched = True
        cd = form.cleaned_data
        temp = float(cd["temperature"])
        hum = float(cd["humidity"])
        ph = float(cd["ph"])
        rain = float(cd["rainfall"])

        # === CHECK FOR IMPOSSIBLE VALUES FIRST ===
        impossible_errors = _check_impossible(temp, hum, ph, rain)
        if impossible_errors:
            impossible = True
            # Don't even run scoring — conditions are physically impossible
        else:
            # === RUN SCORING ===
            scored = []
            for crop in CROPS:
                score = _score_crop(crop, temp, hum, ph, rain)
                if score > 0:
                    scored.append((score, crop))

            scored.sort(key=lambda x: x[0], reverse=True)
            top = scored[:5]  # TOP 5 instead of top 3

            results = [{
                "name": c["name"],
                "season": c["season"],
                "score": s,
                "essentials": [
                    f"Soil pH range: {c['ph_min']}–{c['ph_max']}",
                    f"Temp range: {c['temp_min']}–{c['temp_max']}°C",
                    f"Humidity: {c['hum_min']}–{c['hum_max']}%",
                    f"Rainfall: {c['rain_min']}–{c['rain_max']} mm",
                    f"N requirement: {c['n_need']}",
                ],
                "tips": [
                    "Use balanced NPK as per soil test.",
                    "Maintain proper drainage to avoid root diseases.",
                    "Prefer certified seeds and timely sowing.",
                ]
            } for (s, c) in top]

            if results:
                _track_popularity(request, [r["name"] for r in results])
                messages.success(request, f"{len(results)} crop recommendations generated!")
            # If results is empty, searched=True will trigger the extreme warning

    return render(request, "recommender/manual.html", {
        "active": "manual",
        "form": form,
        "results": results,
        "tips": tips,
        "searched": searched,
        "impossible": impossible,
        "impossible_errors": impossible_errors,
        "crops_url": crops_url,
    })


def auto(request):
    _bump(request, "auto")
    form = AutoCityForm(request.POST or None)
    city_blocks = []

    from django.conf import settings
    import urllib.request, json
    from urllib.parse import quote

    api_key = getattr(settings, "OPENWEATHER_API_KEY", "") or ""
    api_key = api_key.strip()

    def openweather_city(city: str):
        if not api_key:
            return None
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={quote(city)}&appid={api_key}&units=metric"
        )
        try:
            with urllib.request.urlopen(url, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            main = data.get("main", {})
            temp = main.get("temp")
            humidity = main.get("humidity")
            rain_obj = data.get("rain", {}) or {}
            rainfall = rain_obj.get("1h", rain_obj.get("3h", 0.0))
            if temp is None or humidity is None:
                return None
            return {
                "temp": float(temp),
                "humidity": float(humidity),
                "rainfall": float(rainfall),
                "ph": 6.8,
            }
        except Exception:
            return None

    def fake_weather(city):
        base = (sum(ord(ch) for ch in city) % 11) + 18
        return {
            "temp": round(float(base), 1),
            "humidity": round(float((base * 3) % 60 + 35), 1),
            "rainfall": round(float((base * 7) % 180 + 40), 1),
            "ph": 6.8,
        }

    if request.method == "POST" and form.is_valid():
        cities_raw = form.cleaned_data["cities"]
        ph_in = form.cleaned_data.get("ph")
        cities = [c.strip() for c in cities_raw.split(",") if c.strip()]

        for city in cities[:10]:
            w = openweather_city(city) or fake_weather(city)
            if ph_in:
                w["ph"] = float(ph_in)

            scored = []
            for crop in CROPS:
                score = _score_crop(crop, w["temp"], w["humidity"], w["ph"], w["rainfall"])
                if score > 0:
                    scored.append((score, crop))

            scored.sort(key=lambda x: x[0], reverse=True)
            top = scored[:5]  # TOP 5

            block = {
                "city": city,
                "weather": w,
                "top": [{
                    "name": c["name"],
                    "season": c["season"],
                    "score": s,
                    "tips": [
                        "Use mulching to conserve moisture.",
                        "Do seed treatment before sowing.",
                        "Follow integrated pest management (IPM).",
                    ],
                    "essentials": [
                        f"Recommended pH: {c['ph_min']}–{c['ph_max']}",
                        f"N need: {c['n_need']}",
                    ]
                } for (s, c) in top]
            }
            city_blocks.append(block)
            _track_popularity(request, [x["name"] for x in block["top"]])

        messages.success(request, "City based recommendations generated!")

    return render(request, "recommender/auto.html", {
        "active": "auto",
        "form": form,
        "city_blocks": city_blocks
    })


def price(request):
    _bump(request, "price")
    form = PriceForm(request.POST or None)
    result = None

    if request.method == "POST" and form.is_valid():
        crop = form.cleaned_data["crop"].strip().title()
        mandi = form.cleaned_data["mandi"].strip().title()
        seed = sum(ord(x) for x in (crop + mandi)) % 3000
        price_val = 1500 + seed
        trend = "Upward" if seed % 2 == 0 else "Stable"
        result = {
            "crop": crop,
            "mandi": mandi,
            "price": price_val,
            "trend": trend,
            "note": "This is a demo estimate. Connect real mandi API later."
        }
        messages.success(request, "Price fetched successfully!")

    return render(request, "recommender/price.html", {"active": "price", "form": form, "result": result})


def soil(request):
    _bump(request, "soil")
    form = SoilForm(request.POST or None)
    analysis = None

    if request.method == "POST" and form.is_valid():
        ph = form.cleaned_data["ph"]
        moisture = form.cleaned_data["moisture"]

        ph_msg = "Neutral soil (good for most crops)."
        if ph < 6.0:
            ph_msg = "Acidic soil: add lime / organic matter."
        elif ph > 7.5:
            ph_msg = "Alkaline soil: add gypsum / organic compost."

        moisture_msg = "Moisture is adequate."
        if moisture < 30:
            moisture_msg = "Low moisture: irrigate / mulch."
        elif moisture > 75:
            moisture_msg = "High moisture: improve drainage."

        analysis = {
            "ph": ph,
            "moisture": moisture,
            "insights": [ph_msg, moisture_msg],
            "actions": [
                "Do a soil test once per season.",
                "Apply fertilizers based on soil report.",
                "Improve soil structure using compost / FYM.",
            ]
        }
        messages.success(request, "Soil analyzed successfully!")

    return render(request, "recommender/soil.html", {"active": "soil", "form": form, "analysis": analysis})


def crops(request):
    _bump(request, "crops")
    q = (request.GET.get("q") or "").strip().lower()
    data = CROPS
    if q:
        data = [c for c in CROPS if q in c["name"].lower() or q in c["season"].lower()]
    return render(request, "recommender/crops.html", {
        "active": "crops",
        "q": request.GET.get("q", ""),
        "crops": data
    })


def dashboard(request):
    _bump(request, "dashboard")
    usage = request.session.get("usage", {})
    pop = request.session.get("popularity", {})

    top10 = sorted(pop.items(), key=lambda x: int(x[1]), reverse=True)[:10]
    top_labels = [name for name, _ in top10]
    top_values = [int(v) for _, v in top10]
    top_crop_name = top_labels[0] if top_labels else "—"

    counts = {
        "manual": int(usage.get("manual", 0)),
        "auto": int(usage.get("auto", 0)),
        "price": int(usage.get("price", 0)),
        "soil": int(usage.get("soil", 0)),
        "support": int(usage.get("support", 0)),
    }
    total_actions = sum(counts.values())

    last_iso = request.session.get("last_activity")
    last_activity_human = "—"
    if last_iso:
        try:
            dt = timezone.datetime.fromisoformat(last_iso)
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt)
            last_activity_human = f"{timesince(dt)} ago"
        except Exception:
            last_activity_human = "—"

    activity_payload = {
        "labels": ["Manual", "Auto", "Price", "Soil", "Support"],
        "values": [counts["manual"], counts["auto"], counts["price"], counts["soil"], counts["support"]],
    }
    topcrops_payload = {"labels": top_labels, "values": top_values}

    return render(request, "recommender/dashboard.html", {
        "active": "dashboard",
        "counts": counts,
        "total_actions": total_actions,
        "top_crop_name": top_crop_name,
        "last_activity_human": last_activity_human,
        "activity_payload": activity_payload,
        "topcrops_payload": topcrops_payload,
        "top_crops": top10,
        "usage": usage,
        "top10": top10,
    })


def support(request):
    _bump(request, "support")
    form = FeedbackForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        feedbacks = request.session.get("feedbacks", [])
        feedbacks.append(form.cleaned_data)
        request.session["feedbacks"] = feedbacks
        request.session.modified = True
        messages.success(request, "Feedback sent successfully!")
        return redirect("recommender:support")

    return render(request, "recommender/support.html", {"active": "support", "form": form})


# ---------------- AUTH ----------------

def signup_view(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""
        confirm = request.POST.get("confirm_password") or ""

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, "recommender/signup.html", {"active": ""})

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "recommender/signup.html", {"active": ""})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "recommender/signup.html", {"active": ""})

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created! Please login.")
        return redirect("recommender:login")

    return render(request, "recommender/signup.html", {"active": ""})


def login_view(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password.")
            return render(request, "recommender/login.html", {"active": ""})

        login(request, user)
        messages.success(request, "Logged in successfully!")
        return redirect("recommender:home")

    return render(request, "recommender/login.html", {"active": ""})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("recommender:home")


from django.conf import settings
from django.http import JsonResponse
import json
import urllib.request

def navbar_temp(request):
    api_key = getattr(settings, "OPENWEATHER_API_KEY", "") or ""
    if not api_key:
        return JsonResponse({"ok": False, "error": "missing_api_key"}, status=500)

    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "error": "invalid_coords"}, status=400)

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )

    try:
        with urllib.request.urlopen(url, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        temp = data.get("main", {}).get("temp", None)
        if temp is None:
            return JsonResponse({"ok": False, "error": "temp_not_found"}, status=502)
        return JsonResponse({"ok": True, "temp": float(temp)})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=502)