from django import forms
from django.core.validators import RegexValidator
from .models import User, Post

class LogInForm(forms.Form):
    """Form for logging a user into the application."""
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget = forms.PasswordInput)

class SignUpForm(forms.ModelForm):
    """Form for registering a user to the application."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'bio']
        widgets = { 'bio': forms.Textarea() }

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, lowercase character and a number.',
        )],
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Validate form and check if provided passwords match."""
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        """Create and save a new user to the database."""
        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            email = self.cleaned_data.get('email'),
            bio = self.cleaned_data.get('bio'),
            password = self.cleaned_data.get('new_password'),
        )
        return user;

class ProfileUpdateForm(forms.ModelForm):
    """Form for updating a user's information."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio']
        widgets = { 'bio': forms.Textarea() }

class PasswordUpdateForm(forms.Form):
    """Form for updating a user's password."""
    old_password = forms.CharField(label='Current password', widget=forms.PasswordInput())
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, lowercase character and a number.',
        )],
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def __init__(self, user, data=None):
        self.user = user
        super(PasswordUpdateForm, self).__init__(data=data)

    def clean(self):
        """Check if provided passwords match."""
        super().clean()
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            self.add_error('old_password', 'The existing password was incorrect.')
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

class PostForm(forms.ModelForm):
    """Form for creating a new post."""
    class Meta:
        model = Post
        fields = ['text']
        widgets = { 'text': forms.Textarea() }

    def save(self, user):
        post = super().save(commit=False)
        post.author = user
        post.save()
        return post
