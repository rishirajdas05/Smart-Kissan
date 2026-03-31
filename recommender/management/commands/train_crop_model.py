from django.core.management.base import BaseCommand
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import random


class Command(BaseCommand):
    help = "Train Random Voting Crop Classifier (no scikit-learn)"

    def handle(self, *args, **kwargs):
        # recommender/
        APP_DIR = Path(__file__).resolve().parents[2]

        dataset_path = APP_DIR / "dataset" / "Crop_recommendation.csv"
        artifacts_dir = APP_DIR / "ml" / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        if not dataset_path.exists():
            self.stdout.write(self.style.ERROR(f"Dataset not found: {dataset_path}"))
            return

        df = pd.read_csv(dataset_path)

        FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
        LABEL = "label"

        for col in FEATURES + [LABEL]:
            if col not in df.columns:
                self.stdout.write(self.style.ERROR(f"Missing column: {col}"))
                return

        X = df[FEATURES].values.astype(float)
        y_raw = df[LABEL].astype(str).str.lower().values

        # manual label encoding
        unique_labels = sorted(set(y_raw))
        label_to_id = {l: i for i, l in enumerate(unique_labels)}
        id_to_label = {i: l for l, i in label_to_id.items()}
        y = np.array([label_to_id[l] for l in y_raw])

        NUM_RULES = 40
        rules = []

        random.seed(42)
        np.random.seed(42)

        for _ in range(NUM_RULES):
            feat_idx = random.sample(range(len(FEATURES)), 3)

            thresholds = [
                np.random.uniform(X[:, i].min(), X[:, i].max())
                for i in feat_idx
            ]

            mask = np.ones(len(X), dtype=bool)
            for i, t in zip(feat_idx, thresholds):
                mask &= (X[:, i] <= t)

            if mask.sum() == 0:
                dominant = random.choice(list(id_to_label.keys()))
            else:
                dominant = np.bincount(y[mask]).argmax()

            rules.append({
                "features": feat_idx,
                "thresholds": thresholds,
                "label": dominant
            })

        model = {
            "rules": rules,
            "label_map": id_to_label,
            "feature_names": FEATURES
        }

        joblib.dump(model, artifacts_dir / "random_crop_model.joblib")

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Crop model trained successfully | Rules: {NUM_RULES} | Crops: {len(unique_labels)}"
            )
        )
