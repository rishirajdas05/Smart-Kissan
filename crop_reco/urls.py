from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Language switch endpoint
    path("i18n/", include("django.conf.urls.i18n")),

    # Google OAuth + allauth routes
    path("accounts/", include("allauth.urls")),

    # Main app — signup is now the root page (see recommender/urls.py)
    path("", include(("recommender.urls", "recommender"), namespace="recommender")),
]