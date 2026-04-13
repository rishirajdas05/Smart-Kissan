from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .forms import SignupForm, LoginForm

def signup_view(request):
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        u = form.cleaned_data["username"]
        email = form.cleaned_data.get("email") or ""
        p1 = form.cleaned_data["password"]
        p2 = form.cleaned_data["confirm_password"]

        if p1 != p2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=u).exists():
            messages.error(request, "Username already taken.")
        else:
            User.objects.create_user(username=u, email=email, password=p1)
            messages.success(request, "Account created. Please login.")
            return redirect("recommender:login")

    return render(request, "recommender/signup.html", {"active": "signup", "form": form})

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        u = form.cleaned_data["username"]
        p = form.cleaned_data["password"]
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            return redirect("recommender:dashboard")
        messages.error(request, "Invalid credentials.")
    return render(request, "recommender/login.html", {"active": "login", "form": form})

def logout_view(request):
    logout(request)
    return redirect("recommender:home")
