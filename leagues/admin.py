from django.contrib import admin

from .models import League, Season, Team

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