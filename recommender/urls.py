from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "recommender"

urlpatterns = [
    # Root "/" now opens signup page directly
    path("", RedirectView.as_view(pattern_name="recommender:signup", permanent=False)),

    # Home page moved to /home/
    path("home/", views.home, name="home"),

    path("manual/", views.manual, name="manual"),
    path("auto/", views.auto, name="auto"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("price/", views.price, name="price"),
    path("crops/", views.crops, name="crops"),
    path("soil/", views.soil, name="soil"),
    path("support/", views.support, name="support"),
    path("api/navbar-temp/", views.navbar_temp, name="navbar_temp"),

    # Auth
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]