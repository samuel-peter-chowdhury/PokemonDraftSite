from django.template.defaulttags import register
from django.db.models import Subquery
from pokemons.models import DetailedMove

import math
import operator

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_speed(speed, type):
    if type == '0':
        return (speed * 2) + 36
    elif type == '252':
        return math.floor((speed * 2) + 36 + (252/4))
    elif type == '252+':
        return math.floor(((speed * 2) + 36 + (252/4)) * 1.1)
    elif type == '+1':
        return math.floor(math.floor((((speed * 2) + 36 + (252/4)) * 1.1)) * 1.5)
    elif type == '+2':
        return math.floor(math.floor((((speed * 2) + 36 + (252/4)) * 1.1)) * 2)
    
@register.filter
def get_type_effective(pokemon_type_effectives, type):
    for pte in pokemon_type_effectives:
        if pte.type.id == type.id:
            return pte.value
        
@register.filter
def get_stat_color(stat):
    if stat >= 200:
        return '#02ffff'
    elif stat >= 190:
        return '#02ffd4'
    elif stat >= 180:
        return '#02ffaa'
    elif stat >= 170:
        return '#02ff7f'
    elif stat >= 160:
        return '#02ff55'
    elif stat >= 150:
        return '#02ff2a'
    elif stat >= 140:
        return '#2aff08'
    elif stat >= 130:
        return '#66ff00'
    elif stat >= 120:
        return '#9aff00'
    elif stat >= 110:
        return '#ccff00'
    elif stat >= 100:
        return '#fffe00'
    elif stat >= 90:
        return '#ffcc00'
    elif stat >= 80:
        return '#ff9800'
    elif stat >= 70:
        return '#ff6600'
    elif stat >= 60:
        return '#ff3200'
    else:
        return '#ff0000'
    
@register.filter
def get_pokemon_special_move_dictionary(pokemon):
    special_move_dictionary = {}
    special_move_subquery = DetailedMove.objects.exclude(special_category__isnull=True).only('id').all()
    special_moves = pokemon.pokemon_detailed_moves.filter(detailed_move__id__in=Subquery(special_move_subquery))
    for sm in special_moves:
        move = sm.detailed_move
        if move.special_category not in special_move_dictionary:
            special_move_dictionary[move.special_category] = []
        special_move_dictionary[move.special_category].append({'name': move.name, 'category': move.category, 'color': move.type.color, 'id': move.id})
    for key, value in special_move_dictionary.items():
        special_move_dictionary[key] = sorted(value, key = lambda x: (x['color'], x['category'], x['name']))
    return special_move_dictionary

@register.filter
def get_pokemon_coverage_move_dictionary(pokemon):
    coverage_move_dictionary = {}
    coverage_move_subquery = DetailedMove.objects.exclude(viable=False).only('id').all()
    coverage_moves = pokemon.pokemon_detailed_moves.filter(detailed_move__id__in=Subquery(coverage_move_subquery))
    for cm in coverage_moves:
        move = cm.detailed_move
        if move.type.name not in coverage_move_dictionary:
            coverage_move_dictionary[move.type.name] = []
        coverage_move_dictionary[move.type.name].append({'name': move.name, 'category': move.category, 'color': move.type.color, 'id': move.id})
    for key, value in coverage_move_dictionary.items():
        coverage_move_dictionary[key] = sorted(value, key = lambda x: (x['category'], x['name']))
    return coverage_move_dictionary

@register.filter
def get_all_ordered_by(obj, order_by_field):
    return obj.order_by(order_by_field)

@register.filter
def get_remaining_points(team, season):
    points_spent = sum([p.point_value for p in team.pokemons.all()])
    return season.point_limit - points_spent

@register.filter
def get_sorted_keys(dict):
    return sorted(list(dict.keys()))

@register.filter
def get_stat_value_length(value):
    return math.ceil(value * 0.8)

@register.filter
def get_category_icon(category):
    if category == 'physical':
        return 'fa-hand-fist'
    elif category == 'special':
        return 'fa-hand-sparkles'
    else:
        return 'fa-screwdriver-wrench'
    
@register.filter
def even_ternary(value, token_value):
    tokens = token_value.split(',')
    return tokens[0] if value % 2 == 0 else tokens[1]