import requests
import json

from pokemons.models import Pokemon, Type, PokemonType, PokemonTypeEffective, PokemonCoverageMove, PokemonSpecialMove, PokemonMove, PokemonAbility, DetailedMove, PokemonDetailedMove

def initialize_detailed_move_data(season):
    # Initialize special move data
    special_moves_file = open('special_moves.json',)
    special_moves_data = json.load(special_moves_file)
    inverted_special_move_map = {}
    for key, value in special_moves_data.items():
        for move in value:
            inverted_special_move_map[move] = key
    special_moves_file.close()

    # Initialize move data
    moves_file = open('moves.json')
    moves_data = json.load(moves_file)["9"]
    moves_file.close()

    # Initialize pokemon data
    pokemon_file = open('species.json')
    pokemon_data = json.load(pokemon_file)["9"]
    pokemon_file.close()

    # Initialize learnset data
    learnsets_file = open('learnsets.json')
    learnsets_data = json.load(learnsets_file)["9"]
    learnsets_file.close()

    # Initialize move and type map for easy access
    moveMap = {}
    typeMap = {}

    DetailedMove.objects.all().delete()

    index = 1
    for learnsets_key, learnsets_value in learnsets_data.items():
        print(index)
        pokemon_name = pokemon_data[learnsets_key]['name'].lower()
        try:
            pokemon = Pokemon.objects.get(name=pokemon_name, season=season)
        except:
            print(f'********* Failed to retrieve: {pokemon_name} *********')
            continue
        try:
            mega_pokemons = Pokemon.objects.filter(name__contains=pokemon_name + '-mega', season=season)
            if mega_pokemons is not None:
                mega_pokemons = list(mega_pokemons)
                for mp in mega_pokemons:
                    print(f'********* Retrieved mega: {mp.name} *********')
        except:
            pass
        try:
            learnset = learnsets_value['learnset']
        except:
            print(f'********* No learnset: {pokemon_name} *********')
            continue
        for m in learnset.keys():
            m_data = moves_data[m]
            move_name = m_data['name'].lower()
            if move_name in moveMap:
                move = moveMap[move_name]
            else:
                move = DetailedMove()
                move.name = move_name
                move.base_power = m_data['basePower']
                type_name = m_data['type'].lower()
                if type_name in typeMap:
                    type = typeMap[type_name]
                else:
                    type = Type.objects.get(name=type_name)
                    typeMap[type_name] = type
                move.type = type
                move.accuracy = 100 if isinstance(m_data['accuracy'], bool) else m_data['accuracy']
                move.pp = m_data['pp']
                move.priority = m_data['priority']
                move.category = m_data['category'].lower()
                move.special_category = inverted_special_move_map[move_name] if move_name in inverted_special_move_map else None
                move.viable = (move.base_power >= 60 or move.base_power == 0 or 'multihit' in m_data) and (move.accuracy >= 70) and (move.category != 'status')
                move.save()
                moveMap[move_name] = move
            pokemon_detailed_move = PokemonDetailedMove()
            pokemon_detailed_move.pokemon = pokemon
            pokemon_detailed_move.detailed_move = move
            pokemon_detailed_move.save()

            if mega_pokemons is not None and len(mega_pokemons) > 0:
                for mp in mega_pokemons:
                    pokemon_detailed_move = PokemonDetailedMove()
                    pokemon_detailed_move.pokemon = mp
                    pokemon_detailed_move.detailed_move = move
                    pokemon_detailed_move.save()
        index += 1

def initialize_pokemon_data(data, season):
    for p in data:
        pokemon = Pokemon()
        pokemon.name = p['name'].lower()
        pokemon.dex_number = p['dex_number']
        pokemon.hp = p['hp']
        pokemon.attack = p['attack']
        pokemon.defense = p['defense']
        pokemon.special_attack = p['special_attack']
        pokemon.special_defense = p['special_defense']
        pokemon.speed = p['speed']
        pokemon.base_stat_total = pokemon.hp + pokemon.attack + pokemon.defense + pokemon.special_attack + pokemon.special_defense + pokemon.speed
        pokemon.weight = p['weight']
        pokemon.height = p['height']
        sprite = p['sprite']
        response = requests.get(sprite)
        if response.status_code == 200:
            pokemon.sprite_url = sprite
        else:
            pokemon.sprite_url = '/media/defaults/default_pokemon_sprite.png'
        pokemon.season = season
        pokemon.save()

        for t in p['types']:
            type = Type.objects.get(name=t.lower())
            pokemon_type = PokemonType(pokemon=pokemon, type=type)
            pokemon_type.save()

        for a in p['abilities']:
            pokemon_ability = PokemonAbility(pokemon=pokemon)
            pokemon_ability.name = a.lower()
            pokemon_ability.save()

        for m in p['moves']:
            pokemon_move = PokemonMove(pokemon=pokemon)
            pokemon_move.name = m.lower()
            pokemon_move.save()

        for key, value in p['special_moves'].items():
            for m in value:
                pokemon_special_move = PokemonSpecialMove(pokemon=pokemon)
                pokemon_special_move.category = key
                pokemon_special_move.name = m
                pokemon_special_move.save()

        for key, value in p['coverage_moves'].items():
            type = Type.objects.get(name=key.lower())
            for m in value:
                pokemon_coverage_move = PokemonCoverageMove(pokemon=pokemon, type=type)
                pokemon_coverage_move.name = m
                pokemon_coverage_move.save()

        for key, value in p['type_effective'].items():
            type = Type.objects.get(name=key.lower())
            pokemon_type_effective = PokemonTypeEffective(pokemon=pokemon, type=type)
            pokemon_type_effective.value = value
            pokemon_type_effective.save()

def initialize_point_value_data(data, season):
    for line in data:
        pokemon_name = line[0].strip().lower()
        if 'mega ' in pokemon_name:
            suffix = ''
            if ' x' in pokemon_name:
                pokemon_name = pokemon_name.split(' x')[0]
                suffix += '-x'
            if ' y' in pokemon_name:
                pokemon_name = pokemon_name.split(' y')[0]
                suffix += '-y'
            pokemon_name = pokemon_name.split('mega ')[1] + '-mega' + suffix
        if 'galarian ' in pokemon_name:
            pokemon_name = pokemon_name.split('galarian ')[1] + '-galar'
        if 'hisuian ' in pokemon_name:
            pokemon_name = pokemon_name.split('hisuian ')[1] + '-hisui'
        if 'alolan ' in pokemon_name:
            pokemon_name = pokemon_name.split('alolan ')[1] + '-alola'
        if 'paldean ' in pokemon_name:
            suffix = ''
            if ' (fire)' in pokemon_name:
                pokemon_name = pokemon_name.split(' (fire)')[0]
                suffix += '-blaze'
            if ' (water)' in pokemon_name:
                pokemon_name = pokemon_name.split(' (water)')[0]
                suffix += '-aqua'
            pokemon_name = pokemon_name.split('paldean ')[1] + '-paldea' + suffix
        if '-male' in pokemon_name:
            pokemon_name = pokemon_name.split('-male')[0] + '-m'
        if 'urshifu-single-strike' == pokemon_name:
            pokemon_name = 'urshifu'
        if 'ursaluna-bm' == pokemon_name:
            pokemon_name = 'ursaluna-bloodmoon'
        if 'ogerpon-h' == pokemon_name:
            pokemon_name = 'ogerpon-hearthflame'
        if 'ogerpon-c' == pokemon_name:
            pokemon_name = 'ogerpon-cornerstone'
        if 'ogerpon-w' == pokemon_name:
            pokemon_name = 'ogerpon-wellspring'
        if 'ogerpon-t' == pokemon_name:
            pokemon_name = 'ogerpon'
        if 'zygarde-50%' == pokemon_name:
            pokemon_name = 'zygarde'
        if 'lycanroc-midday' == pokemon_name:
            pokemon_name = 'lycanroc'
        if 'oricorio-baile' == pokemon_name:
            pokemon_name = 'oricorio'
        if 'tauros-paldea' == pokemon_name:
            pokemon_name = 'tauros-paldea-combat'
        pokemon = Pokemon.objects.get(season=season, name=pokemon_name)
        pokemon.point_value = int(line[1].strip()) + 1
        pokemon.save()