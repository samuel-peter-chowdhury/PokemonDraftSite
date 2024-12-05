from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    discord_username = models.CharField(max_length=32, blank=True, null=True)
    showdown_username = models.CharField(max_length=19, blank=True, null=True)
    timezone = models.CharField(max_length=5, blank=True, null=True)
    profile_picture = models.ImageField(default='defaults/default_profile_picture.jpg', blank=True, null=True, upload_to='profile_pictures/')

    def __str__(self):
        return self.username
    
    def has_any_league(self):
        return len(self.get_all_leagues()) > 0
    
    def has_league(self, league_id):
        return league_id in [league.id for league in self.get_all_leagues()]
    
    def is_league_member(self, league_id):
        return league_id in [league.id for league in self.member_leagues.all()]
    
    def is_league_moderator(self, league_id):
        return league_id in [league.id for league in self.moderator_leagues.all()]
    
    def get_all_leagues(self):
        return list(set(self.member_leagues.all() | self.moderator_leagues.all()))