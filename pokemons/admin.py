from django.contrib import admin

from .models import Move, Ability, Pokemon, GameStat

# Register your models here.
class MoveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Move._meta.get_fields() if not field.is_relation]
    list_filter = [field.name for field in Move._meta.get_fields() if not field.is_relation]
admin.site.register(Move, MoveAdmin)

class AbilityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Ability._meta.get_fields() if not field.is_relation]
    list_filter = [field.name for field in Ability._meta.get_fields() if not field.is_relation]
admin.site.register(Ability, AbilityAdmin)

class PokemonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Pokemon._meta.get_fields() if not field.is_relation]
    list_filter = [field.name for field in Pokemon._meta.get_fields() if not field.is_relation]
admin.site.register(Pokemon, PokemonAdmin)

class GameStatAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GameStat._meta.get_fields() if not field.is_relation]
    list_filter = [field.name for field in GameStat._meta.get_fields() if not field.is_relation]
admin.site.register(GameStat, GameStatAdmin)