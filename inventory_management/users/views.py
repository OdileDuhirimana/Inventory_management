# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages  

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if request.POST.get('is_staff'):
                user.is_staff = True
                user.save()
            login(request, user)  
            return redirect('home')  
        else:
            print(form.errors)  
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        print(f"Username: {username}, Password: {password}")  
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            print("Authentication failed.")  
            return render(request, 'users/login.html', {'error': 'Invalid credentials.'})
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to a home page or dashboard

@login_required
def home(request):
    return render(request, 'home.html')
