#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Train ML model if not already present
echo "Checking ML model..."
if [ ! -f "ml/artifacts/crop_model.joblib" ]; then
  echo "Training ML model (first deploy)..."
  python train_model_186.py
  echo "ML model trained successfully!"
else
  echo "ML model already exists — skipping training."
fi