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
    STATUS = "status",

class Type(models.TextChoices):
    FIRE = "fire",
    WATER = "water",
    GRASS = "grass",
    ELECTRIC = "electric",
    DARK = "dark",
    GHOST = "ghost",
    DRAGON = "dragon",
    FAIRY = "fairy",
    PSYCHIC = "psychic",
    STEEL = "steel",
    FIGHTING = "fighting",
    BUG = "bug",
    POISON = "poison",
    NORMAL = "normal",
    FLYING = "flying",
    GROUND = "ground",
    ROCK = "rock",
    ICE = "ice",
    
class Move(BaseModel):
    name =  models.CharField(max_length=50, unique=True)
    base_power = models.IntegerField()
    type = models.CharField(max_length=10, choices=Type.choices)
    accuracy = models.IntegerField()
    pp = models.IntegerField()
    priority = models.IntegerField()
    category = models.CharField(max_length=8, choices=MoveCategory.choices)
    description = models.TextField(blank=True, null=True)
    special_categories = models.TextField(blank=True, null=True)
    viable = models.BooleanField()

    def __str__(self):
        return self.name
    
    def get_special_categories(self):
        return self.special_categories.split(',')
    
class Ability(BaseModel):
    name =  models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Pokemon(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    dex_number = models.IntegerField(blank=True, null=True)
    types = models.TextField(blank=True, null=True)
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
    moves = models.ManyToManyField(Move, related_name='pokemons')
    abilities = models.ManyToManyField(Ability, related_name='pokemons')

    def __str__(self):
        return self.name
    
    def get_icon_sprite(self):
        return f'https://play.pokemonshowdown.com/sprites/gen5/{self.name.replace(" ", "-")}.png'
    
    def get_smogon_link(self):
        if '-mega' in self.name:
            return f'https://www.smogon.com/dex/sm/pokemon/{self.sprite_url.split("xy/")[1].split(".gif")[0]}'
        else:
            return f'https://www.smogon.com/dex/sv/pokemon/{self.sprite_url.split("xy/")[1].split(".gif")[0]}'
        
    def get_types(self):
        return self.types.split(',')
        
class TypeEffective(BaseModel):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='type_effectives')
    type = models.CharField(max_length=10, choices=Type.choices)
    value = models.FloatField()

    def __str__(self):
        return f'{self.pokemon}:{self.type}:{self.value}'

class GameStat(BaseModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_stats')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='game_stats')
    direct_kills = models.IntegerField()
    indirect_kills = models.IntegerField()
    deaths = models.IntegerField()