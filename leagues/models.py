from django.db import models

from core.models import BaseModel
from users.models import CustomUser

# Create your models here.
class SeasonStatus(models.TextChoices):
    PRE_SEASON = 'PRE_SEASON'
    DRAFT = 'DRAFT'
    REGULAR_SEASON = 'REGULAR_SEASON'
    PLAYOFFS = 'PLAYOFFS'

class League(BaseModel):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=4)
    logo = models.ImageField(default='defaults/default_league_logo.png', blank=True, null=True, upload_to='league_logos/')
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
    status = models.CharField(max_length=15, choices=SeasonStatus.choices, default=SeasonStatus.PRE_SEASON)
    rules = models.TextField(blank=True, null=True)
    point_limit = models.IntegerField(default=100)
    max_tier_value = models.IntegerField(default=20)

    def __str__(self):
        return self.name

class Team(BaseModel):
    name = models.CharField(max_length=50)
    logo = models.ImageField(default='defaults/default_team_logo.png', blank=True, null=True, upload_to='team_logos/')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='teams')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='teams')

    class Meta:
        unique_together = ('name', 'season')

    def __str__(self):
        return self.name
    
class Week(BaseModel):
    name = models.CharField(max_length=50)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='weeks')
    order = models.IntegerField(default=1)

    class Meta:
        unique_together = ('name', 'season')

    def __str__(self):
        return self.name
    
class Matchup(BaseModel):
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='matchups')
    coach_one = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='coach_one_matchups')
    coach_two = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='coach_two_matchups')
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winner_matchups', blank=True, null=True)
    loser = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='loser_matchups', blank=True, null=True)

    class Meta:
        unique_together = ('week', 'coach_one', 'coach_two')

class Game(BaseModel):
    matchup = models.ForeignKey(Matchup, on_delete=models.CASCADE, related_name='games')
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winner_games')
    loser = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='loser_games')
    differential = models.IntegerField()
    replay_link = models.TextField()