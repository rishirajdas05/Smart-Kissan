#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip

# Install PyJWT first before anything else
pip install PyJWT==2.8.0

pip install -r requirements.txt

# Verify jwt is importable
python -c "import jwt; print('jwt OK:', jwt.__version__)"

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