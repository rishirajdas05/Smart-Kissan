"""
recommender/ml_predict.py

Bridge to existing ML files:
  - recommender/ml/crop_recommender.py  → recommend_top3(N,P,K,T,H,pH,R)
  - recommender/ml/predict.py           → predict_crop(features) fallback
"""


def ml_top_crops(N, P, K, temperature, humidity, ph, rainfall, top_n=5):
    """
    Returns top crops using existing ML pipeline.
    Tries crop_recommender first, then predict.py fallback.
    Returns list of {"name": str, "confidence": float, "source": "ml"}
    """

    # ── Strategy 1: crop_recommender.recommend_top3 ──────────────
    try:
        from recommender.ml.crop_recommender import recommend_top3, ensure_model
        ensure_model()
        top3 = recommend_top3(N, P, K, temperature, humidity, ph, rainfall)

        if top3:
            results = []
            for crop_name, confidence in top3:
                if float(confidence) < 1.0:
                    continue
                results.append({
                    "name":       str(crop_name).title(),
                    "confidence": float(round(confidence, 1)),
                    "source":     "ml",
                })
            if results:
                return results[:top_n]
    except Exception:
        pass

    # ── Strategy 2: predict.py fallback ──────────────────────────
    try:
        from recommender.ml.predict import predict_crop, artifacts_ready
        if artifacts_ready():
            features = [N, P, K, temperature, humidity, ph, rainfall]
            crop_name, confidence = predict_crop(features)
            return [{
                "name":       str(crop_name).title(),
                "confidence": float(round(confidence * 100, 1)),
                "source":     "ml",
            }]
    except Exception:
        pass

    return []


def model_available() -> bool:
    try:
        from recommender.ml.crop_recommender import ensure_model
        return ensure_model()
    except Exception:
        pass
    try:
        from recommender.ml.predict import artifacts_ready
        return artifacts_ready()
    except Exception:
        pass
    return False