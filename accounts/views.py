from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import RegisterForm, LoginForm

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

User = get_user_model()  # Get the custom user model

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        print(f"Trying to authenticate: {email}")  # Debugging

        auth_user = authenticate(request, email=email, password=password)  # ✅ Authenticate using email
        
        if auth_user:
            print("Authentication successful!")
            login(request, auth_user)
            return redirect("home")
        else:
            print("Authentication failed: Incorrect email or password.")
            return render(request, "accounts/login.html", {"error": "Invalid email or password."})

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect('index')
    