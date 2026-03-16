# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from ai_engine.models import UserProfile, GeneratedCourse


# ─────────────────────────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────────────────────────

def home_view(request):
    if not request.user.is_authenticated:
        return render(request, "users/home.html")

    try:
        profile = UserProfile.objects.get(user=request.user)

        if profile.has_completed_assessment():
            courses = GeneratedCourse.objects.filter(user=request.user, is_active=True)
            if courses.exists():
                return redirect("ai_engine:my_courses")
            else:
                return redirect("ai_engine:select_career")
        else:
            return redirect("ai_engine:start_test")

    except UserProfile.DoesNotExist:
        return redirect("ai_engine:start_test")


# ─────────────────────────────────────────────────────────────
#  REGISTER
# ─────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in to continue.")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


# ─────────────────────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email    = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user     = authenticate(request, username=email, password=password)

            if user:
                login(request, user)

                try:
                    profile = UserProfile.objects.get(user=user)

                    if profile.has_completed_assessment():
                        courses = GeneratedCourse.objects.filter(user=user, is_active=True)
                        if courses.exists():
                            messages.success(request, f"Welcome back, {user.email}!")
                            return redirect("ai_engine:my_courses")
                        else:
                            messages.success(request, "Welcome back! Select a career to generate your course.")
                            return redirect("ai_engine:select_career")
                    else:
                        messages.success(request, "Welcome! Let's complete your personality assessment.")
                        return redirect("ai_engine:start_test")

                except UserProfile.DoesNotExist:
                    messages.success(request, "Welcome! Let's get to know you better.")
                    return redirect("ai_engine:start_test")
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


# ─────────────────────────────────────────────────────────────
#  LOGOUT
# ─────────────────────────────────────────────────────────────

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")