import requests

from pokemons.models import Pokemon, Type, PokemonType, PokemonTypeEffective, PokemonCoverageMove, PokemonSpecialMove, PokemonMove, PokemonAbility

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