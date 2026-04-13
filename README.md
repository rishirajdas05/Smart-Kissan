<<<<<<< HEAD
# 🌱 Smart-Kissan — AI Crop Recommendation Platform

## Features
- ✏️ **Manual Recommendation** — Enter soil parameters (N,P,K, pH, humidity, temperature, rainfall) → Get top 3 crops
- 🤖 **Auto Detection** — Enter city → AI fetches weather & soil data → Recommends best crop
- 🪸 **Soil Analyzer** — Enter pH & moisture → Get soil health tips and improvement advice
- 💹 **Crop Prices** — View mandi prices vs MSP for all crops with trend indicators
- 🌾 **Crops Library** — Browse all 25 crops with season, water, duration, and MSP info
- 📊 **Dashboard** — Charts showing your activity, top crops, page visits, and recommendation history
- 👤 **Profile** — Manage your account and farm details
- 💬 **Support** — Contact form with FAQ
- 🌤️ **Live Weather** — Current weather always visible in navbar

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train the ML model
python core/ml_models/train_model.py

# 3. Run migrations
python manage.py migrate

# 4. Start server
python manage.py runserver

# 5. Visit http://127.0.0.1:8000
# Demo login: username=demo, password=demo123
```

## Get Live Weather (Optional)
1. Sign up at https://openweathermap.org/api (free)
2. Copy your API key
3. In `smart_kissan/settings.py`, replace:
   ```python
   OPENWEATHER_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'
   ```
   with your actual key.

## ML Model
- Algorithm: Random Forest Classifier (200 trees)
- Features: N, P, K, Temperature, Humidity, pH, Rainfall
- Crops: 25 Indian crops (rice, wheat, maize, cotton, banana, mango, etc.)
- Training samples: 200 per crop (5000 total)
=======
# CropReco Pro (Django)
Features:
- Crop recommendation (Manual + Auto weather mode)
- Farmer dashboard analytics (charts)
- Multi-language UI (English + Hindi)
- Crop price prediction (baseline model + training command)

## Run
1) Create venv and install:
   pip install -r requirements.txt

2) Copy .env.example -> .env and set OPENWEATHER_API_KEY

3) Migrate + admin:
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser

4) (Optional) Train models:
   python manage.py train_crop_model
   python manage.py train_price_model

5) Start:
   python manage.py runserver

URLs:
- /recommend/manual/
- /recommend/auto/
- /dashboard/ (login required)
- /price/
- /crops/
- /history/
- /feedback/
>>>>>>> 4aecf1fb38a2273c855714379fe153af2ff49375
