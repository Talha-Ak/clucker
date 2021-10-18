from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm

def home(request):
    return render(request, 'home.html')

def feed(request):
    return render(request, 'feed.html')

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
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {'form': form})
