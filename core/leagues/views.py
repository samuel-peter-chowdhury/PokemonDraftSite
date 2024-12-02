from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator

import os
import json
import requests

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
        page = request.GET.get('page', '1')
        pageSize = request.GET.get('page_size', '10')
        orderBy = request.GET.get('order_by', 'name')
        pokemon = Pokemon.objects.defer('pokemon_type_effectives', 'pokemon_coverage_moves', 'pokemon_special_moves', 'pokemon_moves').filter(season=activeSeason).order_by(orderBy)
        p = Paginator(pokemon, pageSize)
        return render(request, "leagues/league.html", {'league': league, 'activeSeason': activeSeason, 'pokemonPage': p.page(page), 'lastPage': p.num_pages, 'pageSize': pageSize, 'orderBy': orderBy})
    else:
        return redirect("/")
    
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