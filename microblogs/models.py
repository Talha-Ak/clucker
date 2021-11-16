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
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='followees'
    )

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to the a small version of the user's gravatar."""
        return self.gravatar(size=60)

    def toggle_follow(self, followee):
        """Toggles whether self follows the given followee."""
        if self.is_following(followee):
            self._unfollow(followee)
        else:
            self._follow(followee)

    def _follow(self, user):
        user.followers.add(self)

    def _unfollow(self, user):
        user.followers.remove(self)

    def is_following(self, user):
        """ Returns whether self follows the given user."""
        return user in self.followees.all()

    def follower_count(self):
        """Returns the number of followers of self."""
        return self.followers.count()

    def followee_count(self):
        """Returns the number of followees of self."""
        return self.followees.count()

class Post(models.Model):
    """The application post model."""
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
