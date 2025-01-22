import requests
import json

from pokemons.models import Pokemon, Move, Ability, TypeEffective
from .models import Week, Matchup, Team

# def export_pokemon_data():
#     data = []
#     pokemon = Pokemon.objects.all()
#     for p in pokemon:
#         p_data = {}
#         p_data['name'] = p.name
#         p_data['dex_number'] = p.dex_number
#         p_data['hp'] = p.hp
#         p_data['attack'] = p.attack
#         p_data['defense'] = p.defense
#         p_data['special_attack'] = p.special_attack
#         p_data['special_defense'] = p.special_defense
#         p_data['speed'] = p.speed
#         p_data['base_stat_total'] = p.base_stat_total
#         p_data['weight'] = p.weight
#         p_data['height'] = p.height
#         p_data['point_value'] = p.point_value
#         p_data['condition'] = p.condition
#         p_data['sprite_url'] = p.sprite_url
#         p_data['season_id'] = p.season.id
#         p_data['team_id'] = p.team.id if p.team is not None else None

#         p_data['types'] = []
#         for t in p.pokemon_types.all():
#             p_data['types'].append(t.type.name)

#         p_data['moves'] = []
#         for m in p.pokemon_detailed_moves.all():
#             p_data['moves'].append(m.detailed_move.name)
        
#         p_data['abilities'] = []
#         for a in p.pokemon_abilities.all():
#             p_data['abilities'].append(a.name)

#         p_data['type_effectives'] = []
#         for te in p.pokemon_type_effectives.all():
#             p_data['type_effectives'].append({'type': te.type.name, 'value': te.value})

#         data.append(p_data)
#     with open('pokemon_db_dump.json', 'w') as f:
#         json.dump(data, f, indent=4)

# def initialize_schedule_data(data, season):
#     # Initialize week map and coach line
#     weekMap = {}
#     teamLine = []

#     # Wipe week data
#     Week.objects.all().delete()

#     for i, line in enumerate(data):
#         if i == 0:
#             teamLine = line
#         else:
#             weekName = line[0]
#             weekMap[weekName] = []
#             for j, cell in enumerate(line):
#                 if j == 0:
#                     pass
#                 else:
#                     weekMap[weekName].append({'coach_one': teamLine[j], 'coach_two': cell})

#     for key, value in weekMap.items():
#         week = Week()
#         week.name = key
#         week.season = season
#         week.save()

#         for pair in value:
#             print(f'{pair["coach_one"]} vs. {pair["coach_two"]}')
#             names = [pair['coach_one'], pair['coach_two']]
#             coaches = Team.objects.filter(name__iregex=r'(' + '|'.join(names) + ')').order_by('name')
#             try:
#                 matchup = Matchup()
#                 matchup.week = week
#                 matchup.coach_one = coaches[0]
#                 matchup.coach_two = coaches[1]
#                 matchup.save()
#             except:
#                 print(f'Duplicate: {week.name}: {coaches[0].name} vs. {coaches[1].name}')

# def initialize_all_pokemon_data(season):
#     # Initialize special move data
#     special_moves_file = open('special_moves.json',)
#     special_moves_data = json.load(special_moves_file)
#     inverted_special_move_map = {}
#     for key, value in special_moves_data.items():
#         for move in value:
#             if move not in inverted_special_move_map:
#                 inverted_special_move_map[move] = []
#             inverted_special_move_map[move].append(key)
#     special_moves_file.close()

#     # Initialize move data
#     moves_file = open('moves.json')
#     moves_data = json.load(moves_file)
#     moves_file.close()

#     # Initialize move data
#     abilities_file = open('abilities.json')
#     abilities_data = json.load(abilities_file)
#     abilities_file.close()

#     # Initialize pokemon data
#     pokemon_file = open('pokemon_db_dump.json')
#     pokemon_data = json.load(pokemon_file)
#     pokemon_file.close()

#     # Initialize move and ability map for easy access
#     moveMap = {}
#     abilityMap = {}

#     # Delete all existing data
#     Move.objects.all().delete()
#     Ability.objects.all().delete()
#     Pokemon.objects.all().delete()

#     # Initialize all moves in json file
#     print('Initializing moves...')
#     size = len(moves_data)
#     for i, m in enumerate(moves_data):
#         print('\r{}/{}'.format(i + 1, size), end='')
#         move = Move()
#         move.name = m['name'].lower()
#         move.base_power = m['power']
#         move.type = m['type'].lower()
#         move.accuracy = m['accuracy']
#         move.pp = m['pp']
#         move.priority = m['priority']
#         category = m['category'].lower()
#         move.category = 'status' if category == 'non-damaging' else category
#         move.description = m['description']
#         move.special_categories = ','.join(inverted_special_move_map[move.name]) if move.name in inverted_special_move_map else None
#         move.viable = (move.base_power >= 60 or move.base_power == 0 or 'times' in move.description) and (move.accuracy >= 70 or move.accuracy == 0) and (move.category != 'status') and ('10,000,000' not in move.name) and ('Z-Power' not in move.description)
#         move.save()
#         moveMap[move.name] = move

#     print('\n')

#     # Initialize all abilities in json file
#     print('Initializing abilities...')
#     size = len(abilities_data)
#     for i, a in enumerate(abilities_data):
#         print('\r{}/{}'.format(i + 1, size), end='')
#         ability = Ability()
#         ability.name = a['name'].lower()
#         ability.description = a['description']
#         ability.save()
#         abilityMap[ability.name] = ability

#     print('\n')

#     print('Initializing pokemon...')
#     size = len(pokemon_data)
#     for i, p in enumerate(pokemon_data):
#         print('\r{}/{}'.format(i + 1, size), end='')
#         pokemon = Pokemon()
#         pokemon.name = p['name']
#         pokemon.dex_number = p['dex_number']
#         pokemon.types = ','.join(p['types'])
#         pokemon.hp = p['hp']
#         pokemon.attack = p['attack']
#         pokemon.defense = p['defense']
#         pokemon.special_attack = p['special_attack']
#         pokemon.special_defense = p['special_defense']
#         pokemon.speed = p['speed']
#         pokemon.base_stat_total = p['base_stat_total']
#         pokemon.weight = p['weight']
#         pokemon.height = p['height']
#         pokemon.point_value = p['point_value']
#         pokemon.condition = p['condition']
#         pokemon.sprite_url = p['sprite_url']
#         pokemon.season = season
#         team = Team.objects.get(id=p['team_id']) if p['team_id'] is not None else None
#         pokemon.team = team
#         pokemon.save()
#         moves = []
#         for m in p['moves']:
#             moves.append(moveMap[m])
#         pokemon.moves.set(moves)
#         abilities = []
#         for a in p['abilities']:
#             abilities.append(abilityMap[a])
#         pokemon.abilities.set(abilities)
#         pokemon.save()

#         for te in p['type_effectives']:
#             type_effective = TypeEffective()
#             type_effective.pokemon = pokemon
#             type_effective.type = te['type']
#             type_effective.value = te['value']
#             type_effective.save()

# def initialize_pokemon_data(data, season):
#     pass
#     for p in data:
#         pokemon = Pokemon()
#         pokemon.name = p['name'].lower()
#         pokemon.dex_number = p['dex_number']
#         pokemon.hp = p['hp']
#         pokemon.attack = p['attack']
#         pokemon.defense = p['defense']
#         pokemon.special_attack = p['special_attack']
#         pokemon.special_defense = p['special_defense']
#         pokemon.speed = p['speed']
#         pokemon.base_stat_total = pokemon.hp + pokemon.attack + pokemon.defense + pokemon.special_attack + pokemon.special_defense + pokemon.speed
#         pokemon.weight = p['weight']
#         pokemon.height = p['height']
#         sprite = p['sprite']
#         response = requests.get(sprite)
#         if response.status_code == 200:
#             pokemon.sprite_url = sprite
#         else:
#             pokemon.sprite_url = '/media/defaults/default_pokemon_sprite.png'
#         pokemon.season = season
#         pokemon.save()

#         for t in p['types']:
#             type = Type.objects.get(name=t.lower())
#             pokemon_type = PokemonType(pokemon=pokemon, type=type)
#             pokemon_type.save()

#         for a in p['abilities']:
#             pokemon_ability = PokemonAbility(pokemon=pokemon)
#             pokemon_ability.name = a.lower()
#             pokemon_ability.save()

#         for m in p['moves']:
#             pokemon_move = PokemonMove(pokemon=pokemon)
#             pokemon_move.name = m.lower()
#             pokemon_move.save()

#         for key, value in p['special_moves'].items():
#             for m in value:
#                 pokemon_special_move = PokemonSpecialMove(pokemon=pokemon)
#                 pokemon_special_move.category = key
#                 pokemon_special_move.name = m
#                 pokemon_special_move.save()

#         for key, value in p['coverage_moves'].items():
#             type = Type.objects.get(name=key.lower())
#             for m in value:
#                 pokemon_coverage_move = PokemonCoverageMove(pokemon=pokemon, type=type)
#                 pokemon_coverage_move.name = m
#                 pokemon_coverage_move.save()

#         for key, value in p['type_effective'].items():
#             type = Type.objects.get(name=key.lower())
#             pokemon_type_effective = PokemonTypeEffective(pokemon=pokemon, type=type)
#             pokemon_type_effective.value = value
#             pokemon_type_effective.save()

# def initialize_point_value_data(data, season):
#     pass
#     for line in data:
#         pokemon_name = line[0].strip().lower()
#         if 'mega ' in pokemon_name:
#             suffix = ''
#             if ' x' in pokemon_name:
#                 pokemon_name = pokemon_name.split(' x')[0]
#                 suffix += '-x'
#             if ' y' in pokemon_name:
#                 pokemon_name = pokemon_name.split(' y')[0]
#                 suffix += '-y'
#             pokemon_name = pokemon_name.split('mega ')[1] + '-mega' + suffix
#         if 'galarian ' in pokemon_name:
#             pokemon_name = pokemon_name.split('galarian ')[1] + '-galar'
#         if 'hisuian ' in pokemon_name:
#             pokemon_name = pokemon_name.split('hisuian ')[1] + '-hisui'
#         if 'alolan ' in pokemon_name:
#             pokemon_name = pokemon_name.split('alolan ')[1] + '-alola'
#         if 'paldean ' in pokemon_name:
#             suffix = ''
#             if ' (fire)' in pokemon_name:
#                 pokemon_name = pokemon_name.split(' (fire)')[0]
#                 suffix += '-blaze'
#             if ' (water)' in pokemon_name:
#                 pokemon_name = pokemon_name.split(' (water)')[0]
#                 suffix += '-aqua'
#             pokemon_name = pokemon_name.split('paldean ')[1] + '-paldea' + suffix
#         if '-male' in pokemon_name:
#             pokemon_name = pokemon_name.split('-male')[0] + '-m'
#         if 'urshifu-single-strike' == pokemon_name:
#             pokemon_name = 'urshifu'
#         if 'ursaluna-bm' == pokemon_name:
#             pokemon_name = 'ursaluna-bloodmoon'
#         if 'ogerpon-h' == pokemon_name:
#             pokemon_name = 'ogerpon-hearthflame'
#         if 'ogerpon-c' == pokemon_name:
#             pokemon_name = 'ogerpon-cornerstone'
#         if 'ogerpon-w' == pokemon_name:
#             pokemon_name = 'ogerpon-wellspring'
#         if 'ogerpon-t' == pokemon_name:
#             pokemon_name = 'ogerpon'
#         if 'zygarde-50%' == pokemon_name:
#             pokemon_name = 'zygarde'
#         if 'lycanroc-midday' == pokemon_name:
#             pokemon_name = 'lycanroc'
#         if 'oricorio-baile' == pokemon_name:
#             pokemon_name = 'oricorio'
#         if 'tauros-paldea' == pokemon_name:
#             pokemon_name = 'tauros-paldea-combat'
#         pokemon = Pokemon.objects.get(season=season, name=pokemon_name)
#         pokemon.point_value = int(line[1].strip()) + 1
#         pokemon.save()