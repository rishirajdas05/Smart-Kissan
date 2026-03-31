from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import csv

APP_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = APP_DIR / "dataset"

@dataclass(frozen=True)
class CropItem:
    name: str

def _fallback_crops() -> List[CropItem]:
    names = [
        "rice", "maize", "chickpea", "kidneybeans", "pigeonpeas", "mothbeans",
        "mungbean", "blackgram", "lentil", "pomegranate", "banana", "mango",
        "grapes", "watermelon", "muskmelon", "apple", "orange", "papaya",
        "coconut", "cotton", "jute", "coffee"
    ]
    return [CropItem(n) for n in names]

def get_all_crops() -> List[CropItem]:
    """
    Tries to read labels from any csv in recommender/dataset that has a 'label' column.
    Otherwise returns fallback list.
    """
    if not DATASET_DIR.exists():
        return _fallback_crops()

    # find a csv that contains "label" column (common in Crop_recommendation.csv)
    for csv_path in DATASET_DIR.glob("*.csv"):
        try:
            with csv_path.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    continue
                cols = {c.strip().lower() for c in reader.fieldnames}
                if "label" in cols:
                    items = []
                    for row in reader:
                        val = (row.get("label") or "").strip()
                        if val:
                            items.append(val.lower())
                    items = sorted(set(items))
                    if items:
                        return [CropItem(x) for x in items]
        except Exception:
            continue

    return _fallback_crops()

def get_crop_detail(name: str) -> dict:
    """
    Minimal detail for UI. You can extend later.
    """
    n = (name or "").strip().lower()
    return {
        "name": n,
        "season": "Kharif / Rabi (varies by region)",
        "ph_range": "6.0 – 7.5",
        "notes": "Details can be extended from dataset later."
    }
