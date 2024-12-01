from django.db import models

from core.models import BaseModel
from users.models import CustomUser

# Create your models here.
class League(BaseModel):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=4)
    logo = models.ImageField(default='default_league_logo.png', blank=True)
    password = models.CharField(max_length=20)
    members = models.ManyToManyField(CustomUser, related_name='member_leagues')
    moderators = models.ManyToManyField(CustomUser, related_name='moderator_leagues')
