from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    username = models.EmailField(max_length=50, unique=True, blank=False)  # email

