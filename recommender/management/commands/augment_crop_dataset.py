from django.core.management.base import BaseCommand
from pathlib import Path
import pandas as pd
import numpy as np

class Command(BaseCommand):
    help = "Create a bigger (synthetic) crop dataset by adding small noise to existing rows."

    def add_arguments(self, parser):
        parser.add_argument("--target", type=int, default=50000, help="Target rows (default 50000)")
        parser.add_argument("--out", type=str, default="Crop_recommendation_augmented.csv", help="Output filename in recommender/dataset/")

    def handle(self, *args, **options):
        target = int(options["target"])
        out_name = options["out"]

        base = Path(__file__).resolve().parents[3]  # recommender/
        dataset_path = base / "dataset" / "Crop_recommendation.csv"
        out_path = base / "dataset" / out_name

        if not dataset_path.exists():
            self.stdout.write(self.style.ERROR(f"Dataset not found: {dataset_path}"))
            return

        df = pd.read_csv(dataset_path)
        if len(df) == 0:
            self.stdout.write(self.style.ERROR("Dataset is empty."))
            return

        reps = int(np.ceil(target / len(df)))
        big = pd.concat([df] * reps, ignore_index=True).sample(frac=1.0, random_state=42).reset_index(drop=True)
        big = big.iloc[:target].copy()

        # Add small Gaussian noise (synthetic). Keep within safe ranges.
        rng = np.random.default_rng(42)

        def jitter(col, std, minv=None, maxv=None):
            x = big[col].astype(float).to_numpy()
            x = x + rng.normal(0, std, size=len(x))
            if minv is not None: x = np.maximum(x, minv)
            if maxv is not None: x = np.minimum(x, maxv)
            big[col] = x

        jitter("N", 2.0, 0, None)
        jitter("P", 2.0, 0, None)
        jitter("K", 2.0, 0, None)
        jitter("temperature", 0.4, -10, 60)
        jitter("humidity", 0.8, 0, 100)
        jitter("ph", 0.05, 0, 14)
        jitter("rainfall", 1.8, 0, None)

        big.to_csv(out_path, index=False)
        self.stdout.write(self.style.SUCCESS(f"✅ Created augmented dataset: {out_path} ({len(big)} rows)"))
        self.stdout.write(self.style.WARNING("Note: This is synthetic augmentation (good for demo/training, not a substitute for real field data)."))
