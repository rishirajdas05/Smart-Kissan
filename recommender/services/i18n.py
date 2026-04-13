# recommender/services/i18n.py

LANGUAGES = [
    ("en", "English"),
    ("hi", "Hindi"),
    ("bn", "Bengali"),
    ("te", "Telugu"),
    ("mr", "Marathi"),
    ("ta", "Tamil"),
]

# Small UI dictionary (NO API KEY needed for this style of translation)
_TRANSLATIONS = {
    "en": {
        "home": "Home",
        "manual": "Manual",
        "auto": "Auto",
        "dashboard": "Dashboard",
        "price": "Price",
        "crops": "Crops",
        "soil": "Soil",
        "support": "Support",
        "start_manual": "Start Manual Mode",
        "try_auto": "Try Auto (City Only)",
        "fetch_recommend": "Fetch & Recommend",
        "reset": "Reset",
        "recommend_top3": "Recommend Top 3",
    },
    "hi": {
        "home": "होम",
        "manual": "मैनुअल",
        "auto": "ऑटो",
        "dashboard": "डैशबोर्ड",
        "price": "कीमत",
        "crops": "फसलें",
        "soil": "मिट्टी",
        "support": "सहायता",
        "start_manual": "मैनुअल मोड शुरू करें",
        "try_auto": "ऑटो आज़माएँ (केवल शहर)",
        "fetch_recommend": "लाओ और सुझाओ",
        "reset": "रीसेट",
        "recommend_top3": "टॉप 3 सुझाएँ",
    },
    # Other languages can stay English until you expand
    "bn": {},
    "te": {},
    "mr": {},
    "ta": {},
}


def get_lang(request):
    return request.session.get("lang", "en")


def set_lang(request, lang_code: str):
    allowed = {c for c, _ in LANGUAGES}
    request.session["lang"] = lang_code if lang_code in allowed else "en"


def get_tr(lang_code: str):
    base = _TRANSLATIONS.get("en", {})
    other = _TRANSLATIONS.get(lang_code, {}) or {}
    merged = dict(base)
    merged.update(other)
    return merged
