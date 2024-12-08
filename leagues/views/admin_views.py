from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse

import json
import csv

from leagues.forms import PokemonSimpleSearchForm, DataUploadForm
from leagues.models import League, Team
from leagues.data import initialize_pokemon_data, initialize_point_value_data
from pokemons.models import Pokemon

@user_passes_test(lambda u: u.is_superuser)
def initialize_pokemon_data_view(request, id):
    league = League.objects.get(id=id)
    activeSeason = league.get_active_season()
    if request.method == "POST":
        form = DataUploadForm(request.POST, request.FILES)
        if form.is_valid() and activeSeason:
            file = request.FILES['file']
            data = json.load(file)
            initialize_pokemon_data(data, activeSeason)
    else:
        form = DataUploadForm()
    return render(request, "leagues/admin/initialize_pokemon_data.html", { "form": form, 'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id) })

@user_passes_test(lambda u: u.is_superuser)
def initialize_point_data_view(request, id):
    league = League.objects.get(id=id)
    activeSeason = league.get_active_season()
    if request.method == "POST":
        form = DataUploadForm(request.POST, request.FILES)
        if form.is_valid() and activeSeason:
            file = request.FILES['file']
            decoded_file = file.read().decode('utf-8').splitlines()
            tsv_file = csv.reader(decoded_file, delimiter="\t")
            initialize_point_value_data(tsv_file, activeSeason)
    else:
        form = DataUploadForm()
    return render(request, "leagues/admin/initialize_point_data.html", { "form": form, 'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id) })

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
    
@login_required(login_url="/users/login/")
def admin_modify_tiers_view(request, id):
    if request.user.has_league(id) and request.user.is_league_moderator(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        tiers = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        return render(request, "leagues/admin/modify_tiers.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason, 'tiers': tiers})
    else:
        return redirect("/")

@login_required(login_url="/users/login/")
def get_admin_modify_tier(request, league_id, tier):
    if request.user.has_league(league_id) and request.user.is_league_moderator(league_id):
        if request.method == "POST":
            pokemon_id = request.GET.get('pokemonId', None)
            point_value = request.POST['point_value']
            p = Pokemon.objects.get(id=pokemon_id)
            p.point_value = point_value
            p.save()
        league = League.objects.get(id=league_id)
        activeSeason = league.get_active_season()
        orderBy = request.GET.get('order_by', 'name')
        pokemon = Pokemon.objects.defer('pokemon_type_effectives', 'pokemon_coverage_moves', 'pokemon_special_moves', 'pokemon_moves').filter(season=activeSeason, point_value=tier).order_by(orderBy)
        return render(request, "leagues/admin/modify_tier.html", {'league': league, 'tier': tier, 'pokemon': pokemon, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)