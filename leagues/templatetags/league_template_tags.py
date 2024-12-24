from django.template.defaulttags import register

import math

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
    for sm in pokemon.pokemon_special_moves.all().order_by('name'):
        if sm.category not in special_move_dictionary:
            special_move_dictionary[sm.category] = []
        special_move_dictionary[sm.category].append(sm.name)
    return special_move_dictionary

@register.filter
def get_pokemon_coverage_move_dictionary(pokemon):
    coverage_move_dictionary = {}
    for cm in pokemon.pokemon_coverage_moves.all().order_by('name'):
        if cm.type.name not in coverage_move_dictionary:
            coverage_move_dictionary[cm.type.name] = []
        coverage_move_dictionary[cm.type.name].append({'name': cm.name, 'color': cm.type.color})
    return coverage_move_dictionary