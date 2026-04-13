from django.core.management.base import BaseCommand
from pathlib import Path
import pandas as pd
import joblib


class Command(BaseCommand):
    help = "Train price model without sklearn (supports price_inr_per_quintal, month/year)"

    def handle(self, *args, **kwargs):
        # recommender/
        APP_DIR = Path(__file__).resolve().parents[2]

        dataset_path = APP_DIR / "dataset" / "crop_prices_sample.csv"
        artifacts_dir = APP_DIR / "ml" / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        if not dataset_path.exists():
            self.stdout.write(self.style.ERROR(f"Price dataset not found: {dataset_path}"))
            return

        df = pd.read_csv(dataset_path)
        df.columns = [c.strip() for c in df.columns]

        # ✅ detect crop column
        crop_col = "crop" if "crop" in df.columns else None
        if not crop_col:
            self.stdout.write(self.style.ERROR(f"Missing crop column. Available columns: {list(df.columns)}"))
            return

        # ✅ detect price column (NOW includes your column)
        price_candidates = [
            "price", "Price",
            "modal_price", "Modal_Price",
            "avg_price", "Avg_Price",
            "price_inr_per_quintal",   # ✅ your column
            "price_inr", "price_in_rs",
            "rate", "Rate",
        ]
        price_col = None
        for c in price_candidates:
            if c in df.columns:
                price_col = c
                break

        if not price_col:
            self.stdout.write(self.style.ERROR("❌ Could not detect required price column."))
            self.stdout.write(self.style.ERROR(f"Available columns: {list(df.columns)}"))
            self.stdout.write(self.style.ERROR("Expected one of: " + ", ".join(price_candidates)))
            return

        # ✅ month + year exist in your dataset
        if "month" not in df.columns:
            self.stdout.write(self.style.ERROR(f"Missing 'month' column. Available columns: {list(df.columns)}"))
            return

        # cleanup
        df[crop_col] = df[crop_col].astype(str).str.lower().str.strip()
        df[price_col] = pd.to_numeric(df[price_col], errors="coerce")
        df["month"] = pd.to_numeric(df["month"], errors="coerce")

        df = df.dropna(subset=[crop_col, price_col, "month"])
        df = df[(df["month"] >= 1) & (df["month"] <= 12)]
        df = df[df[crop_col] != ""]

        # Train: monthly avg price per crop
        price_table = {}
        for crop in df[crop_col].unique():
            cdf = df[df[crop_col] == crop]
            monthly_avg = cdf.groupby("month")[price_col].mean().to_dict()
            price_table[crop] = {int(m): float(v) for m, v in monthly_avg.items()}

        model = {
            "type": "monthly",
            "crop_col": crop_col,
            "price_col": price_col,
            "prices": price_table,
        }

        out_path = artifacts_dir / "price_model.joblib"
        joblib.dump(model, out_path)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Price model trained | Crops: {len(price_table)} | Saved: {out_path}"
        ))
