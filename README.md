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
