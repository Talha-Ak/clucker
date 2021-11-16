from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm, PostForm, ProfileUpdateForm, PasswordUpdateForm
from .models import User, Post
from .helpers import login_prohibited

@login_prohibited
def home(request):
    """View for getting the homepage"""
    return render(request, 'home.html')

@login_prohibited
def log_in(request):
    """View for getting the login page, and for posting the completed login form"""
    if request.method == 'POST':
        form = LogInForm(request.POST)
        next = request.POST.get('next') or '';
        # Check the validation of username and password
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            # Check if user exists with username-password combination.
            if user is not None:
                login(request, user)
                redirect_url = next or 'feed'
                return redirect(redirect_url)
        messages.add_message(request, messages.ERROR, "The username/password provided were invalid.")
    else:
        next = request.GET.get('next') or '';
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form, 'next': next})

def log_out(request):
    """View for getting the log out page, which redirects to home."""
    logout(request)
    return redirect(home)

@login_prohibited
def sign_up(request):
    """View for getting the sign up page, and for posting the completed form>"""
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

@login_required
def feed(request):
    """View for getting the user's main feed."""
    form = PostForm()
    current_user = request.user
    posts = Post.objects.filter(author=current_user)
    return render(request, 'feed.html', {'form': form, 'posts': posts})

@login_required
def follow_toggle(request, user_id):
    current_user = request.user
    try:
        followee = User.objects.get(id=user_id)
        current_user.toggle_follow(followee)
    except User.DoesNotExist:
        return redirect('user_list')
    else:
        return redirect('show_user', user_id=user_id)

def new_post(request):
    """View for posting a Post from a user."""
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
    """View for getting the user list page."""
    return render(request, 'user_list.html', { 'users': User.objects.filter(is_superuser=False) })

@login_required
def show_user(request, user_id):
    """View for getting a specific user's page."""
    try:
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(author=user)
        return render(request, 'show_user.html', { 'user': user, 'posts': posts })
    except User.DoesNotExist:
        return redirect('user_list')

@login_required
def update_profile(request):
    """View for getting update profile page, and posting update form."""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        # Check the validation of the form, and update user if OK.
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Your profile was updated.")
            return redirect('feed')
    # If a GET request, create new form.
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def update_password(request):
    """View for getting update password page, and posting update form."""
    if request.method == 'POST':
        form = PasswordUpdateForm(request.user, request.POST)
        # Check the validation of the form, and update user if OK.
        if form.is_valid():
            request.user.set_password(form.cleaned_data.get('new_password'))
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.add_message(request, messages.SUCCESS, "Your password was updated.")
            return redirect('feed')
    # If a GET request, create new form.
    else:
        form = PasswordUpdateForm(request.user)
    return render(request, 'update_password.html', {'form': form})
