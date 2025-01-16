from django.contrib import admin

from .models import League, Season, Team, Week, Matchup, Game

# Register your models here.
class LeagueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in League._meta.get_fields() if not field.is_relation]
    list_filter = [field.name for field in League._meta.get_fields() if not field.is_relation]
admin.site.register(League, LeagueAdmin)

class SeasonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Season._meta.get_fields() if not field.is_relation]
    list_filter = [field.name for field in Season._meta.get_fields() if not field.is_relation]
admin.site.register(Season, SeasonAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Team._meta.get_fields() if not field.is_relation]
    list_filter = [field.name for field in Team._meta.get_fields() if not field.is_relation]
admin.site.register(Team, TeamAdmin)

class WeekAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Week._meta.get_fields() if not field.is_relation]
    list_filter = [field.name for field in Week._meta.get_fields() if not field.is_relation]
admin.site.register(Week, WeekAdmin)

class MatchupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Matchup._meta.get_fields() if not field.is_relation]
    list_filter = [field.name for field in Matchup._meta.get_fields() if not field.is_relation]
admin.site.register(Matchup, MatchupAdmin)

class GameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Game._meta.get_fields() if not field.is_relation]
    list_filter = [field.name for field in Game._meta.get_fields() if not field.is_relation]
admin.site.register(Game, GameAdmin)