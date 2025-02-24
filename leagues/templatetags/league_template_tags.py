from django.template.defaulttags import register

import math

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_speed(speed, type):
    match type:
        case '0':
            return (speed * 2) + 36
        case '252':
            return math.floor((speed * 2) + 36 + (252/4))
        case '252+':
            return math.floor(((speed * 2) + 36 + (252/4)) * 1.1)
        case '+1':
            return math.floor(math.floor((((speed * 2) + 36 + (252/4)) * 1.1)) * 1.5)
        case '+2':
            return math.floor(math.floor((((speed * 2) + 36 + (252/4)) * 1.1)) * 2)
        case _:
            return 0
        
@register.filter
def get_type_color(type):
    match type:
        case 'fire':
            return '#EE8130'
        case 'water':
            return '#6390F0'
        case 'grass':
            return '#7AC74C'
        case 'electric':
              return '#F7D02C'
        case 'dark':
              return '#705746'
        case 'ghost':
              return '#735797'
        case 'dragon':
            return '#6F35FC'
        case 'fairy':
            return '#D685AD'
        case 'psychic':
            return '#F95587'
        case 'steel':
            return '#B7B7CE'
        case 'fighting':
            return '#C22E28'
        case 'bug':
            return '#A6B91A'
        case 'poison':
            return '#A33EA1'
        case 'normal':
            return '#A8A77A'
        case 'flying':
            return '#A98FF3'
        case 'ground':
            return '#E2BF65'
        case 'rock':
            return '#B6A136'
        case 'ice':
            return '#96D9D6'
        case _:
            return 'white'
        
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
def get_type_effective_color(value):
    if value >= 4:
        return '#F07470'
    elif value >= 2:
        return '#F1959B'
    elif value >= 1:
        return '#C5E8B7'
    elif value >= 0.5:
        return '#ABE098'
    else:
        return '#83D475'

@register.filter
def get_type_effective_total_color(total):
    if total >= 8:
        return '#2EB62C'
    elif total >= 6:
        return '#57C84D'
    elif total >= 4:
        return '#83D475'
    elif total >= 2:
        return '#ABE098'
    elif total >= 0:
        return '#C5E8B7'
    elif total >= -2:
        return '#F1959B'
    elif total >= -4:
        return '#F07470'
    elif total >= -6:
        return '#EA4C46'
    else:
        return '#DC1C13'

@register.filter
def get_all_ordered_by(obj, order_by_field):
    return obj.order_by(order_by_field)

@register.filter
def get_remaining_points(team, season):
    points_spent = sum([p.point_value for p in team.pokemons.all()])
    return season.point_limit - points_spent

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

@register.filter
def get_pokemon_standing_size(place):
    if place == 1:
        return 5
    else:
        return max(1, 5 - place)
    
@register.filter
def get_team_standing_color(place):
    winning_color = (58, 116, 43)
    losing_color = (153, 0, 0)
    if place <= 10:
        return lighten_color(*winning_color, place / 12)
    else:
        return lighten_color(*losing_color, (-1 * (place - 17)) / 8)

def lighten_color(r, g, b, factor):
    return tuple(int(c + (255 - c) * factor) for c in (r, g, b))

@register.filter
def get_speed_position(speed, minMaxSpeed):
    tokens = minMaxSpeed.split(',')
    min_speed = int(tokens[0])
    max_speed = int(tokens[1])
    return ((speed - min_speed) / (max_speed - min_speed)) * 100

@register.filter
def match_outcome_color(team, winner):
    return '#3C6930' if team.id == winner.id else '#AA4A44'

@register.filter
def game_outcome_color(team, winner):
    return '#5fa64c' if team.id == winner.id else '#c5726d'

@register.filter
def game_diff_symbol(team, winner):
    return '+' if team.id == winner.id else '-'