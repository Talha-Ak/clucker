from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm, PostForm
from .models import User        # Can this dependency be avoided?

def home(request):
    """View for GETting the homepage"""
    return render(request, 'home.html')

def feed(request):
    """View for GETting the user's main feed."""
    form = PostForm()
    return render(request, 'feed.html', {'form': form})

def new_post(request):
    """View for POSTing a Post from a user."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        # Only save message if user logged in and within post text limit.
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, "You need to be logged in to make a post.")
        elif form.is_valid():
            form.save(request.user)
            form = PostForm()
        return render(request, 'feed.html', {'form': form})

def user_list(request):
    """View for GETting the user list page."""
    return render(request, 'user_list.html', { 'users': User.objects.filter(is_superuser=False) })

def show_user(request, user_id):
    """View for GETting a specific user's page."""
    return render(request, 'show_user.html', { 'user': User.objects.get(id=user_id) })

def log_in(request):
    """View for GETting the login page, and for POSTing the completed login form"""
    if request.method == 'POST':
        form = LogInForm(request.POST)
        # Check the validation of username and password
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            # Check if user exists with username-password combination.
            if user is not None:
                login(request, user)
                return redirect('feed')
        messages.add_message(request, messages.ERROR, "The username/password provided were invalid.")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    """View for GETting the log out page, which redirects to home."""
    logout(request)
    return redirect(home)

def sign_up(request):
    """View for GETting the sign up page, and for POSTing the completed form>"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # Check the validation of the form, and sign up user if OK.
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    # If a GET request, create new form.
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
