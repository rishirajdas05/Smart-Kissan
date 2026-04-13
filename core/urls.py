from django.urls import path
from . import views

urlpatterns = [
    # Core pages
    path('', views.home, name='home'),
    path('manual/', views.manual_recommend, name='manual'),
    path('auto/', views.auto_recommend, name='auto'),
    path('soil-analyzer/', views.soil_analyzer, name='soil_analyzer'),
    path('crop-prices/', views.crop_prices, name='crop_prices'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('crops/', views.crops_list, name='crops_list'),
    path('profile/', views.profile, name='profile'),
    path('support/', views.support, name='support'),

    # ── Feature 1: AI Chat ───────────────────────────────────────────────────
    path('chat/', views.ai_chat, name='ai_chat'),
    path('api/chat/', views.chat_api, name='chat_api'),

    # ── Feature 2: Crop Calendar ─────────────────────────────────────────────
    path('calendar/', views.crop_calendar, name='crop_calendar'),

    # ── Feature 5: 7-day Forecast ────────────────────────────────────────────
    path('forecast/', views.weather_forecast, name='weather_forecast'),

    # ── Feature 6: Yield Estimator ───────────────────────────────────────────
    path('yield-estimator/', views.yield_estimator, name='yield_estimator'),

    # ── Feature 7: Mandi Locator ─────────────────────────────────────────────
    path('mandi/', views.mandi_locator, name='mandi_locator'),

    # ── Feature 9: PDF Export ────────────────────────────────────────────────
    path('export/recommendation/<int:rec_id>/', views.export_recommendation_pdf, name='export_pdf'),

    # ── Feature 11: Feedback ─────────────────────────────────────────────────
    path('api/feedback/', views.submit_feedback, name='submit_feedback'),

    # ── APIs ─────────────────────────────────────────────────────────────────
    path('api/weather/', views.get_weather_api, name='weather_api'),
    path('api/set-language/', views.set_language, name='set_language'),
]