from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from .forms import UserForm, CalculationForm, OperationSelectionForm
from .task import handle_calculation, send_otp_email, send_operation_notification, get_users_by_operation
import random

def signup(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.otp = str(random.randint(100000, 999999))
            user.email_verified = False
            user.save()
            send_otp_email(user.email, user.otp)
            return redirect('verify_otp', user_id=user.id)
    return render(request, 'signup.html', {'form': form})

def verify_otp(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        if user.otp == request.POST['otp']:
            user.email_verified = True
            user.otp = None  
            user.save()
            login(request, user)
            return redirect('signin')
        return render(request, 'verify_otp.html', {'error': 'Invalid OTP', 'user_id': user_id})
    return render(request, 'verify_otp.html', {'user_id': user_id})

def signin(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'signin.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    return redirect('signin')

@login_required
def home(request):
    return render(request, "home.html")

@login_required
def calci(request):
    form = CalculationForm(request.POST or None)
    result = handle_calculation(request.user, form.cleaned_data['num1'], form.cleaned_data['num2'], form.cleaned_data['operation']) if form.is_valid() else None
    return render(request, 'add.html', {'form': form, 'result': result})

def fetch_users_by_operation(request):
    form = OperationSelectionForm(request.POST or None)
    users, email_sent = [], False
    
    if request.method == "POST":
        if "get_users" in request.POST:
            fetched_users, fetched_emails = get_users_by_operation(form)
            users = list(zip(fetched_users, fetched_emails))  # Combine into list of tuples
            request.session["emails"] = fetched_emails
        elif "send_email" in request.POST:
            email_sent = send_operation_notification(request.session.get("emails", []))
    
    return render(request, "operation_user.html", {"form": form, "users": users, "email_sent": email_sent})
