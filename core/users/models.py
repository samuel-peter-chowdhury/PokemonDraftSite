from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    discord_username = models.CharField(max_length=32, blank=True)
    showdown_username = models.CharField(max_length=19, blank=True)
    timezone = models.CharField(max_length=5, blank=True)
    profile_picture = models.ImageField(default='default_profile_picture.jpg', blank=True)

    def __str__(self):
        return self.username