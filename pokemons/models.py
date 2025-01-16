from django.db import models

from core.models import BaseModel
from leagues.models import Season, Team, Game

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
    STATUS = "status",

class MoveCategory(models.TextChoices):
    PHYSICAL = "physical",
    SPECIAL = "special",
    STATUS = "status"

class Pokemon(BaseModel):
    name = models.CharField(max_length=50, unique=True)
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
    
    def get_smogon_link(self):
        if '-mega' in self.name:
            return f'https://www.smogon.com/dex/sm/pokemon/{self.sprite_url.split("xy/")[1].split(".gif")[0]}'
        else:
            return f'https://www.smogon.com/dex/sv/pokemon/{self.sprite_url.split("xy/")[1].split(".gif")[0]}'

class Type(BaseModel):
    name = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name
    
class DetailedMove(BaseModel):
    name =  models.CharField(max_length=50, unique=True)
    base_power = models.IntegerField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='detailed_moves')
    accuracy = models.IntegerField()
    pp = models.IntegerField()
    priority = models.IntegerField()
    category = models.CharField(max_length=8, choices=MoveCategory.choices)
    special_category = models.CharField(max_length=16, choices=SpecialMoveCategory.choices, blank=True, null=True)
    viable = models.BooleanField()

    def __str__(self):
        return self.name

class PokemonDetailedMove(BaseModel):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon_detailed_moves')
    detailed_move = models.ForeignKey(DetailedMove, on_delete=models.CASCADE, related_name='pokemon_detailed_moves')

    def __str__(self):
        return f'{self.pokemon}:{self.detailed_move}'


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

class GameStat(BaseModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_stats')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='pokemon_game_stats')
    direct_kills = models.IntegerField()
    indirect_kills = models.IntegerField()
    deaths = models.IntegerField()