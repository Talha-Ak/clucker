from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .forms import SignUpForm, LogInForm, PostForm, ProfileUpdateForm, PasswordUpdateForm
from .models import User, Post
from .helpers import login_prohibited

@login_prohibited
def home(request):
    """View for getting the homepage"""
    return render(request, 'home.html')

class LogInView(View):
    """View that handles log in."""

    http_method_names = ['get', 'post']

    @method_decorator(login_prohibited)
    def dispatch(self, request):
        return super().dispatch(request)

    def get(self, request):
        """Display log in template."""
        next = request.GET.get('next') or '';
        return self.render(next)

    def post(self, request):
        """Handle log in attempt."""
        form = LogInForm(request.POST)
        next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(next)
        messages.add_message(request, messages.ERROR, "The username/password provided were invalid.")
        return self.render(next)

    def render(self, next):
        """Render log in template with log in form."""
        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': next})

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
    authors = list(current_user.followees.all()) + [current_user]
    posts = Post.objects.filter(author__in=authors)
    return render(request, 'feed.html', {'form': form, 'user': current_user, 'posts': posts})

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

class UserListView(ListView):
    """View that shows a list of all users."""
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

    @method_decorator(login_required)
    def dispatch(self, request):
        return super().dispatch(request)

class ShowUserView(DetailView):
    """View that shows individual user details."""
    model = User
    template_name = 'show_user.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Generate content to be displayed in the template."""
        context = super().get_context_data(*args, **kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(author=user)
        context['following'] = self.request.user.is_following(user)
        context['followable'] = (self.request.user != user)
        return context

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
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
