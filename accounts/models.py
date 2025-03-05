from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # ✅ Ensure login is done via email
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

