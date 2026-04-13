#!/usr/bin/env bash
set -o errexit

<<<<<<< HEAD
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   Smart-Kissan Build Script"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️  Running migrations..."
python manage.py migrate

# Train ML model (pkl files are gitignored so must retrain)
echo "🤖 Training ML model (119 crops)..."
python core/ml_models/train_model.py

# Create demo user if not exists
echo "👤 Setting up demo user..."
python manage.py shell -c "
from django.contrib.auth.models import User
from core.models import UserProfile
if not User.objects.filter(username='demo').exists():
    u = User.objects.create_user('demo', 'demo@smartkissan.in', 'demo1234', first_name='Demo')
    UserProfile.objects.get_or_create(user=u, defaults={'city': 'Indore', 'state': 'Madhya Pradesh'})
    print('Demo user created: demo / demo1234')
else:
    print('Demo user already exists')
"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   ✅ Build completed successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
=======
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
>>>>>>> 4aecf1fb38a2273c855714379fe153af2ff49375
