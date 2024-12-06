from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse
from django.conf import settings

import os
import json
import csv

from leagues.forms import PokemonSimpleSearchForm
from leagues.models import League, Season, Team
from leagues.data import initialize_pokemon_data, initialize_point_value_data
from pokemons.models import Pokemon

@user_passes_test(lambda u: u.is_superuser)
def initialize_season_view(request, id):
    if request.method == "POST":
        season = Season.objects.get(id=id)
        if season:
            with open(os.path.join(settings.BASE_DIR, 'pokemon_data.json'), 'r') as f:
                data = json.load(f)
                initialize_pokemon_data(data)
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
                initialize_point_value_data(tsv_file)
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)
    return HttpResponse(status=400)

@login_required(login_url="/users/login/")
def modify_team_view(request, id):
    if request.user.has_league(id) and request.user.is_league_moderator(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        return render(request, "leagues/admin/modify_team.html", {'league': league, 'teams': activeSeason.teams.all(), 'isLeagueModerator': request.user.is_league_moderator(league.id)})
    else:
        return redirect("/")
    
@login_required(login_url="/users/login/")
def get_modifiable_team_view(request, league_id, team_id):
    if request.user.has_league(league_id) and request.user.is_league_moderator(league_id):
        team = Team.objects.get(id=team_id)
        if request.method == "POST":
            action = request.GET.get('action', None)
            pokemon_id = request.GET.get('pokemonId', None)
            print(action, pokemon_id)
            if action and pokemon_id:
                pokemon = Pokemon.objects.get(id=pokemon_id)
                if action == 'add':
                    pokemon.team = team
                if action == 'remove':
                    pokemon.team = None
                pokemon.save()
        league = League.objects.get(id=league_id)
        pokemon = team.pokemons.all()
        total_points = sum([p.point_value for p in pokemon])
        form = PokemonSimpleSearchForm()
        return render(request, "leagues/admin/modifiable_team.html", {"form": form, 'league': league, "team": team, "pokemon": pokemon, "totalPoints": total_points})
    else:
        return redirect("/")
    
@login_required(login_url="/users/login/")
def admin_simple_search_results(request, league_id, team_id):
    if request.user.has_league(league_id) and request.user.is_league_moderator(league_id):
        league = League.objects.get(id=league_id)
        team = Team.objects.get(id=team_id)
        activeSeason = league.get_active_season()
        if request.method == "POST":
            form = PokemonSimpleSearchForm(data=request.POST)
            if form.is_valid():
                pokemon_objects = Pokemon.objects.filter(season=activeSeason, point_value__isnull=False)
                for f in form.fields:
                    pokemon_objects = pokemon_objects.filter(**{f: form.cleaned_data[f]})
                pokemon = pokemon_objects.distinct().order_by('name')[:10]
        else: 
            form = PokemonSimpleSearchForm()
        return render(request, "leagues/admin/simple_search_results.html", {'form': form, 'league': league, "team": team, 'undraftedPokemon': pokemon})
    else:
        return HttpResponse(status=400)