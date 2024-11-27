# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ParameterForm, HospitalParameterForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django.db import IntegrityError

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']
        try:
            user = User.objects.create_user(username=username, password=password)
            user.profile.user_type = user_type  # Set the user type on the profile
            user.save()
            return redirect('login')
        except IntegrityError:
            return render(request, 'main/signup.html', {'error': 'Username already exists.'})
    return render(request, 'main/signup.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    if user.profile.user_type == 'patient':
                        login(request, user)
                        return redirect('home')
                except Profile.DoesNotExist:
                    return render(request, 'main/login.html', {'form': form, 'error': 'Profile does not exist.'})
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def hospital_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    if user.profile.user_type == 'hospital':
                        login(request, user)
                        return redirect('hospital_home')
                    else:
                        return render(request, 'main/hospital_login.html', {'form': form, 'error': 'Invalid user type.'})
                except Profile.DoesNotExist:
                    return render(request, 'main/hospital_login.html', {'form': form, 'error': 'Profile does not exist.'})
            else:
                return render(request, 'main/hospital_login.html', {'form': form, 'error': 'Invalid credentials.'})
    else:
        form = AuthenticationForm()
    return render(request, 'main/hospital_login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def home(request):
    result = None
    if request.method == 'POST':
        form = ParameterForm(request.POST)
        if form.is_valid():
            # Placeholder for prediction logic
            inputs = [form.cleaned_data[key] for key in form.cleaned_data]
            result = sum(inputs)  # Replace with actual model prediction
    else:
        form = ParameterForm()
    return render(request, 'main/home.html', {'form': form, 'result': result})

@login_required
def hospital_home(request):
    result = None
    if request.method == 'POST':
        form = HospitalParameterForm(request.POST)
        if form.is_valid():
            # Placeholder for prediction logic
            inputs = [form.cleaned_data[key] for key in form.cleaned_data]
            result = sum(inputs)  # Replace with actual model prediction
    else:
        form = HospitalParameterForm()
    return render(request, 'main/hospital_home.html', {'form': form, 'result': result})


def chatbot_api(request):
    # Your logic here
    return JsonResponse({'message': 'Hello, this is the chatbot API'})

def landing(request):
    return render(request, 'main/landing.html')