from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm
from .models import User        # Can this dependency be avoided?

def home(request):
    return render(request, 'home.html')

def feed(request):
    return render(request, 'feed.html')

def user_list(request):
    return render(request, 'user_list.html', { 'users': User.objects.filter(is_superuser=False) })

def show_user(request, user_id):
    return render(request, 'show_user.html', { 'user': User.objects.get(id=user_id) })

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
        messages.add_message(request, messages.ERROR, "The username/password provided were invalid.")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect(home)

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
