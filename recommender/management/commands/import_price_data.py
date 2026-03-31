from django.core.management.base import BaseCommand
from pathlib import Path
import pandas as pd
from recommender.ml.models import CropPriceRecord

class Command(BaseCommand):
    help = "Import crop price CSV into database (CropPriceRecord)."

    def handle(self, *args, **options):
        base = Path(__file__).resolve().parents[3]  # recommender/
        dataset_path = base / "dataset" / "crop_prices_sample.csv"
        if not dataset_path.exists():
            self.stdout.write(self.style.ERROR(f"Price dataset not found: {dataset_path}"))
            return

        df = pd.read_csv(dataset_path)
        required = ["crop","year","month","price_inr_per_quintal"]
        for c in required:
            if c not in df.columns:
                self.stdout.write(self.style.ERROR(f"Missing column: {c}"))
                return

        CropPriceRecord.objects.all().delete()

        objs = []
        for _, r in df.iterrows():
            objs.append(CropPriceRecord(
                crop=str(r["crop"]).strip().lower(),
                market=str(r.get("market","") or "").strip(),
                year=int(r["year"]),
                month=int(r["month"]),
                price_inr_per_quintal=float(r["price_inr_per_quintal"]),
            ))
        CropPriceRecord.objects.bulk_create(objs, batch_size=2000)
        self.stdout.write(self.style.SUCCESS(f"✅ Imported {len(objs)} price rows into database."))
