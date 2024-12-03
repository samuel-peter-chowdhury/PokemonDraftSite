from django.db import models

from core.models import BaseModel
from users.models import CustomUser

# Create your models here.
class SeasonStatus(models.TextChoices):
    DRAFT = 'DRAFT'
    REGULAR_SEASON = 'REGULAR_SEASON'
    PLAYOFFS = 'PLAYOFFS'

class League(BaseModel):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=4)
    logo = models.ImageField(default='default_league_logo.png', blank=True, null=True)
    password = models.CharField(max_length=20)
    members = models.ManyToManyField(CustomUser, related_name='member_leagues')
    moderators = models.ManyToManyField(CustomUser, related_name='moderator_leagues')

    def __str__(self):
        return self.name
    
    def get_active_season(self):
        return next((season for season in self.seasons.all() if season.is_active), None)

class Season(BaseModel):
    name = models.CharField(max_length=50)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='seasons')
    status = models.CharField(max_length=15, choices=SeasonStatus.choices, default=SeasonStatus.DRAFT)

    def __str__(self):
        return self.name

class Team(BaseModel):
    name = models.CharField(max_length=50)
    logo = models.ImageField(default='default_team_logo.png', blank=True, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='teams')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.name