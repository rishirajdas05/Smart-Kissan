from __future__ import annotations
from pathlib import Path
from typing import List, Dict
import joblib
import pandas as pd

APP_DIR = Path(__file__).resolve().parents[1]
ART_DIR = APP_DIR / "ml" / "artifacts"

DEFAULT_COLS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

def _load_model():
    candidates = [
        "crop_model.joblib", "crop_model.pkl",
        "model.joblib", "model.pkl",
        "rf_model.joblib", "rf_model.pkl",
    ]
    for name in candidates:
        p = ART_DIR / name
        if p.exists():
            return joblib.load(p)
    return None

_MODEL = None

def recommend_top3(features: dict) -> List[Dict]:
    """
    Returns list like: [{"name":"rice","score":92.1}, ...]
    Never returns tuples (prevents your template crash).
    """
    global _MODEL
    if _MODEL is None:
        _MODEL = _load_model()

    # Make DF with correct feature names to avoid sklearn warning
    model = _MODEL
    cols = DEFAULT_COLS
    if model is not None and hasattr(model, "feature_names_in_"):
        cols = list(model.feature_names_in_)

    row = [float(features.get(c, 0.0)) for c in cols]
    X = pd.DataFrame([row], columns=cols)

    # If model missing, fallback dummy recommendation
    if model is None:
        # simple fallback heuristic
        ph = float(features.get("ph", 7.0))
        rain = float(features.get("rainfall", 100.0))
        if rain > 150:
            base = ["rice", "jute", "banana"]
        elif ph < 6:
            base = ["potato", "tea", "coffee"]
        else:
            base = ["maize", "cotton", "mungbean"]
        return [{"name": n, "score": s} for n, s in zip(base, [88.0, 82.0, 76.0])]

    # Predict probabilities
    proba = model.predict_proba(X)[0]
    labels = list(getattr(model, "classes_", []))

    pairs = list(zip(labels, proba))
    pairs.sort(key=lambda x: x[1], reverse=True)
    top = pairs[:3]

    # Convert to dicts (FIXES your tuple template crash)
    out = []
    for name, p in top:
        out.append({"name": str(name), "score": round(float(p) * 100.0, 2)})
    return out
