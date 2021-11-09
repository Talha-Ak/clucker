from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm, PostForm
from .models import User, Post
from .helpers import login_prohibited

@login_prohibited
def home(request):
    """View for GETting the homepage"""
    return render(request, 'home.html')

@login_required
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
        elif not form.is_valid():
            messages.add_message(request, messages.ERROR, "Your post is too long. Maximum length is 280 characters.")
        else:
            form.save(request.user)
        return redirect('feed')

@login_required
def user_list(request):
    """View for GETting the user list page."""
    return render(request, 'user_list.html', { 'users': User.objects.filter(is_superuser=False) })

@login_required
def show_user(request, user_id):
    """View for GETting a specific user's page."""
    try:
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(author=user)
        return render(request, 'show_user.html', { 'user': user, 'posts': posts })
    except User.DoesNotExist:
        return redirect('user_list')

@login_prohibited
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
                redirect_url = request.POST.get('next') or 'feed';
                return redirect(redirect_url)
        messages.add_message(request, messages.ERROR, "The username/password provided were invalid.")
    form = LogInForm()
    next = request.GET.get('next') or '';
    return render(request, 'log_in.html', {'form': form, 'next': next})

def log_out(request):
    """View for GETting the log out page, which redirects to home."""
    logout(request)
    return redirect(home)

@login_prohibited
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
