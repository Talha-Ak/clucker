from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from .forms import SignUpForm, LogInForm, PostForm, ProfileUpdateForm, PasswordUpdateForm
from .models import User, Post
from .helpers import login_prohibited, LoginProhibitedMixin

@login_prohibited
def home(request):
    """View for getting the homepage"""
    return render(request, 'home.html')


class LogInView(LoginProhibitedMixin, View):
    """View that handles log in."""
    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

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


class SignUpView(LoginProhibitedMixin, FormView):
    """View that signs up user"""
    form_class = SignUpForm
    template_name = 'sign_up.html'
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


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


class UserListView(LoginRequiredMixin, ListView):
    """View that shows a list of all users."""
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'


class ShowUserView(LoginRequiredMixin, DetailView):
    """View that shows individual user details."""
    model = User
    template_name = 'show_user.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'

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


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View to update logged-in user's profile."""
    model = ProfileUpdateForm
    template_name = 'update_profile.html'
    form_class = ProfileUpdateForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Your profile was updated.")
        return reverse('feed')


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
