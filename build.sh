#!/usr/bin/env bash
set -o errexit

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   Smart-Kissan Build Script"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🗄️  Running migrations..."
python manage.py migrate

echo "🤖 Training ML model (119 crops)..."
python core/ml_models/train_model.py

echo "🔥 Pre-loading ML model into cache..."
python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_kissan.settings')
django.setup()
from core.ml_engine import _load, predict_crop
_load()
r = predict_crop(80, 48, 40, 24, 82, 6.4, 236)
print(f'ML model loaded OK — test prediction: {r[0][\"crop\"]} ({r[0][\"confidence\"]}%)')
"

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