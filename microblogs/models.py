from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from libgravatar import Gravatar

class User(AbstractUser):
    """The application user model, also used for user authenticaion."""
    username = models.CharField(
        unique=True,
        blank=False,
        max_length=30,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username does not meet required format. (@ followed by at least 3 characters)',
        )],
    )
    first_name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=50)
    email = models.EmailField(unique=True, blank=False)
    bio = models.CharField(unique=False, blank=True, max_length=520)

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url


class Post(models.Model):
    """The application post model."""
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
