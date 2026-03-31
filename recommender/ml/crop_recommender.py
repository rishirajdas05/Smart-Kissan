# recommender/ml/crop_recommender.py
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Global variables to hold model and encoders
_MODEL = None
_LABEL_ENCODER = None
_AVAILABLE_CROPS = []

CSV_CANDIDATES = [
    "Crop_recommendation.csv",
    "crop_recommendation.csv",
    "Crop_recommendation_augmented_50000.csv",
    "Crop_recommendation_sample.csv",
]

def _find_dataset():
    """
    Search for a dataset CSV in likely locations.
    """
    base_dirs = [
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # recommender/ml/
        os.path.dirname(os.path.abspath(__file__)),  # recommender/ml/
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),  # project root
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset"),  # recommender/ml/dataset
    ]
    for base in base_dirs:
        for name in CSV_CANDIDATES:
            path = os.path.join(base, name)
            if os.path.isfile(path):
                return path
    return None

def _train_model(df):
    """
    Train RandomForest on provided dataset.
    Expect columns: N, P, K, temperature, humidity, ph, rainfall, label (crop)
    Adjust based on actual csv.
    """
    global _MODEL, _LABEL_ENCODER, _AVAILABLE_CROPS
    # Example column names; change if dataset differs
    feature_cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    # Identify crop label column (assuming last column is crop name)
    label_col = [c for c in df.columns if c.lower() in ["label", "crop", "target"]]
    if not label_col:
        label_col = df.columns[-1]
    else:
        label_col = label_col[0]

    # Clean and prepare
    df_clean = df.dropna(subset=feature_cols + [label_col])
    X = df_clean[feature_cols].astype(float)
    y = df_clean[label_col].astype(str)

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    # Simple RF with default params
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y_enc)

    _MODEL = rf
    _LABEL_ENCODER = le
    _AVAILABLE_CROPS = list(le.classes_)

def _load_or_train():
    """
    Load dataset if present, otherwise train a trivial fallback.
    """
    dataset_path = _find_dataset()
    if dataset_path:
        try:
            df = pd.read_csv(dataset_path)
            _train_model(df)
            return True
        except Exception:
            # Fall through to fallback
            pass

    # Fallback: tiny synthetic dataset
    # Columns: N, P, K, temperature, humidity, ph, rainfall, crop
    data = [
        [90, 40, 40, 25, 65, 6.8, 120, "maize"],
        [60, 30, 30, 28, 70, 6.5, 100, "rice"],
        [50, 50, 50, 22, 60, 7.0, 80, "coffee"],
        [70, 35, 35, 24, 55, 6.6, 90, "jute"],
        [80, 40, 40, 26, 50, 6.9, 110, "watermelon"],
    ]
    df = pd.DataFrame(data, columns=[
        "N", "P", "K", "temperature", "humidity", "ph", "rainfall", "crop"
    ])
    _train_model(df)
    return False  # indicates fallback used

def ensure_model():
    """
    Public helper to ensure model is ready; returns True if real dataset used.
    """
    if _MODEL is None:
        return _load_or_train()
    return bool(_AVAILABLE_CROPS)

def recommend_top3(N, P, K, temperature, humidity, ph, rainfall):
    """
    Returns list of three tuples: (crop_name, confidence_percent)
    """
    ensure_model()
    # Build input array
    X = np.array([[N, P, K, temperature, humidity, ph, rainfall]], dtype=float)
    if _MODEL is None:
        return []

    probs = _MODEL.predict_proba(X)[0]
    # Get top 3
    idx_sorted = np.argsort(probs)[::-1][:3]
    crops = _LABEL_ENCODER.inverse_transform(idx_sorted)
    confidences = (probs[idx_sorted] * 100).round(1)
    return list(zip(crops, confidences))

def available_crops():
    ensure_model()
    return list(_AVAILABLE_CROPS)
