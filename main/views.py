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
from .test3 import predict  # Import the predict function from the Python script
from django.views.decorators.csrf import csrf_exempt
import json

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'default_user_type')  # Provide a default value
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
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'main/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def hospital_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('hospital_home')
            else:
                return render(request, 'main/hospital_login.html', {'form': form, 'error': 'Invalid username or password'})
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
    if request.method == 'POST':
        form = HospitalParameterForm(request.POST)
        if form.is_valid():
            # Extract the form data
            data = [form.cleaned_data[key] for key in form.cleaned_data]
            # Process the input data using the predict function from the Python script
            chances = predict(data)
            return JsonResponse({'chances': chances})
    else:
        form = HospitalParameterForm()
    return render(request, 'main/hospital_home.html', {'form': form})

def result_view(request, result):
    result = float(result)  # Convert the result to float
    return render(request, 'main/result.html', {'result': result})

def chatbot_api(request):
    # Your logic here
    return JsonResponse({'message': 'Hello, this is the chatbot API'})

def landing(request):
    return render(request, 'main/landing.html')



@csrf_exempt
def process_parameters(request):
    if request.method == 'POST':
        try:
            # Log raw request body
            print("Raw request body:", request.body)

            data = json.loads(request.body)
            print("Parsed data:", data)

            features = data.get('features', [])
            print("Features received:", features)

            if len(features) != 22:
                raise ValueError("Exactly 22 parameters are required.")

            # Call the prediction function
            prediction = predict(features)
            print("Prediction result:", prediction)

            return JsonResponse({"status": "success", "prediction": prediction})
        except Exception as e:
            print("Error occurred:", str(e))  # Log the error
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method."})
