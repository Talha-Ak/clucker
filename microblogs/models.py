from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(
        unique=True,
        blank=False,
        max_length=30,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username does not meet required format. (@ followed by at least 3 characters)',
        )],
    )

    first_name = models.CharField(
        blank=False,
        max_length=50,
    )

    last_name = models.CharField(
        blank=False,
        max_length=50,
    )

    email = models.EmailField(
        unique=True,
        blank=False,
    )

    bio = models.CharField(
        unique=False,
        blank=True,
        max_length=520,
    )
