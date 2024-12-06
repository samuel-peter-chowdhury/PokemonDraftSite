from django.db import models

from core.models import BaseModel
from leagues.models import Season, Team

# Create your models here.
class SpecialMoveCategory(models.TextChoices):
    MOMENTUM = "momentum",
    RECOVERY = "recovery",
    CLERIC = "cleric",
    HAZARD = "hazard",
    HAZARD_REMOVAL = "hazard removal",
    DISRUPTION = "disruption",
    DAMAGE_REDUCTION = "damage reduction",
    SET_UP = "set up",
    PRIORITY = "priority",
    ITEM_REMOVAL = "item removal",
    STATUS = "status"

class Pokemon(BaseModel):
    name = models.CharField(max_length=50)
    dex_number = models.IntegerField(blank=True, null=True)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special_attack = models.IntegerField()
    special_defense = models.IntegerField()
    speed = models.IntegerField()
    base_stat_total = models.IntegerField()
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    point_value = models.IntegerField(blank=True, null=True)
    condition = models.TextField(blank=True, null=True)
    sprite_url = models.TextField(blank=True, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='pokemons')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='pokemons', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_icon_sprite(self):
        return f'https://play.pokemonshowdown.com/sprites/gen5/{self.name.replace(" ", "-")}.png'

class Type(BaseModel):
    name = models.CharField(max_length=10)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class PokemonType(BaseModel):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon_types')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='pokemon_types')

    def __str__(self):
        return f'{self.pokemon}:{self.type}'

class PokemonTypeEffective(BaseModel):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon_type_effectives')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='pokemon_type_effectives')
    value = models.FloatField()

    def __str__(self):
        return f'{self.pokemon}:{self.type}:{self.value}'

class PokemonCoverageMove(BaseModel):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon_coverage_moves')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='pokemon_coverage_moves')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.pokemon}:{self.type}:{self.name}'
    
class PokemonSpecialMove(BaseModel):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon_special_moves')
    category = models.CharField(max_length=16, choices=SpecialMoveCategory.choices)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.pokemon}:{self.category}:{self.name}'

class PokemonMove(BaseModel):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon_moves')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.pokemon}:{self.name}'

class PokemonAbility(BaseModel):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon_abilities')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.pokemon}:{self.name}'