#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Force reinstall PyJWT to fix allauth jwt import issue
pip install --force-reinstall PyJWT==2.8.0

python manage.py collectstatic --no-input
python manage.py migrate

# Train ML model if not present
echo "Checking ML model..."
if [ ! -f "ml/artifacts/crop_model.joblib" ]; then
  echo "Training ML model..."
  python train_model_186.py
  echo "ML model trained!"
else
  echo "ML model exists — skipping."
fi