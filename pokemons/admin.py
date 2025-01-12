from django.contrib import admin

from .models import Pokemon, Type, PokemonType, PokemonTypeEffective, PokemonCoverageMove, PokemonSpecialMove, PokemonMove, PokemonAbility, DetailedMove, PokemonDetailedMove

# Register your models here.
class PokemonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Pokemon._meta.get_fields() if not field.is_relation]
admin.site.register(Pokemon, PokemonAdmin)

class DetailedMoveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DetailedMove._meta.get_fields() if not field.is_relation]
admin.site.register(DetailedMove, DetailedMoveAdmin)

class PokemonDetailedMoveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PokemonDetailedMove._meta.get_fields() if not field.is_relation]
admin.site.register(PokemonDetailedMove, PokemonDetailedMoveAdmin)

class TypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Type._meta.get_fields() if not field.is_relation]
admin.site.register(Type, TypeAdmin)

class PokemonTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PokemonType._meta.get_fields() if not field.is_relation]
admin.site.register(PokemonType, PokemonTypeAdmin)

class PokemonTypeEffectiveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PokemonTypeEffective._meta.get_fields() if not field.is_relation]
admin.site.register(PokemonTypeEffective, PokemonTypeEffectiveAdmin)

class PokemonCoverageMoveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PokemonCoverageMove._meta.get_fields() if not field.is_relation]
admin.site.register(PokemonCoverageMove, PokemonCoverageMoveAdmin)

class PokemonSpecialMoveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PokemonSpecialMove._meta.get_fields() if not field.is_relation]
admin.site.register(PokemonSpecialMove, PokemonSpecialMoveAdmin)

class PokemonMoveAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PokemonMove._meta.get_fields() if not field.is_relation]
admin.site.register(PokemonMove, PokemonMoveAdmin)

class PokemonAbilityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PokemonAbility._meta.get_fields() if not field.is_relation]
admin.site.register(PokemonAbility, PokemonAbilityAdmin)