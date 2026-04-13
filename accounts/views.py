from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username   = request.POST.get('username')
        email      = request.POST.get('email')
        password   = request.POST.get('password')
        confirm    = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name', '')
        last_name  = request.POST.get('last_name', '')
        if password != confirm:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name
            )
            login(request, user)
            messages.success(request, f'Welcome to Smart-Kissan, {first_name or username}!')
            return redirect('home')
    return render(request, 'accounts/signup.html')