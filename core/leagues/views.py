from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator

import os
import json
import requests
import csv

from .forms import LeagueCreationForm
from .models import League, Season
from pokemons.models import Pokemon, Type, PokemonType, PokemonTypeEffective, PokemonCoverageMove, PokemonSpecialMove, PokemonMove, PokemonAbility, SpecialMoveCategory

# Create your views here.
@user_passes_test(lambda u: u.is_superuser)
def create_view(request):
    if request.method == "POST":
        form = LeagueCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else: 
        form = LeagueCreationForm()
    return render(request, "leagues/create.html", { "form": form })

def league_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        return render(request, "leagues/league.html", {'league': league, 'activeSeason': activeSeason})
    else:
        return redirect("/")
    
def league_pokemon_list_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        page = request.GET.get('page', '1')
        pageSize = request.GET.get('page_size', '10')
        orderBy = request.GET.get('order_by', 'name')
        pokemon = Pokemon.objects.defer('pokemon_type_effectives', 'pokemon_coverage_moves', 'pokemon_special_moves', 'pokemon_moves').filter(season=activeSeason).order_by(orderBy)
        p = Paginator(pokemon, pageSize)
        return render(request, "leagues/league_pokemon_list.html", {'league': league, 'activeSeason': activeSeason, 'pokemonPage': p.page(page), 'lastPage': p.num_pages, 'pageSize': pageSize, 'orderBy': orderBy})
    else:
        return redirect("/")
    
def league_pokemon_tiers_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        tiers = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        return render(request, "leagues/league_pokemon_tiers.html", {'league': league, 'activeSeason': activeSeason, 'tiers': tiers})
    else:
        return redirect("/")
    
def get_tier(request, league_id, tier):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
        activeSeason = league.get_active_season()
        orderBy = request.GET.get('order_by', 'name')
        pokemon = Pokemon.objects.defer('pokemon_type_effectives', 'pokemon_coverage_moves', 'pokemon_special_moves', 'pokemon_moves').filter(season=activeSeason, point_value=tier).order_by(orderBy)
        return render(request, "leagues/league_pokemon_tier.html", {'league': league, 'tier': tier, 'pokemon': pokemon, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)
    
@user_passes_test(lambda u: u.is_superuser)
def initialize_season_view(request, id):
    if request.method == "POST":
        season = Season.objects.get(id=id)
        if season:
            with open(os.path.join(settings.BASE_DIR, 'pokemon_data.json'), 'r') as f:
                data = json.load(f)
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
                        pokemon.sprite_url = '/media/default_pokemon_sprite.png'
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

            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=400)

@user_passes_test(lambda u: u.is_superuser)
def initialize_point_data_view(request, id):
    if request.method == "POST":
        season = Season.objects.get(id=id)
        if season:
            with open(os.path.join(settings.BASE_DIR, 'point_data.tsv'), 'r') as f:
                tsv_file = csv.reader(f, delimiter="\t")
                for line in tsv_file:
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
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=400)