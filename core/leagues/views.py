from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q

import os
import json
import csv
import functools

from .forms import PokemonSearchForm, LeagueJoinForm, TeamForm, PokemonSimpleSearchForm
from .models import League, Season, Team
from .data import initialize_pokemon_data, initialize_point_value_data
from pokemons.models import Pokemon, Type
from django.contrib import messages

# Create your views here.
@login_required(login_url="/users/login/")
def league_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        return render(request, "leagues/league.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason})
    return redirect(reverse('users:settings'))

@login_required(login_url="/users/login/")
def league_join_view(request):
    if request.method == "POST":
        form = LeagueJoinForm(request.POST)
        if form.is_valid():
            league = League.objects.filter(name__iexact=form.cleaned_data["league_name"]).first()
            if league:
                if league.password == form.cleaned_data["league_password"]:
                    active_season = league.get_active_season()
                    team_names = [t.name.lower() for t in active_season.teams.all()]
                    if form.cleaned_data["team_name"].lower() in team_names:
                        messages.error(request, 'Team Name Already Exists')
                    else:
                        league.members.add(request.user)
                        league.save()
                        request.user.member_leagues.add(league)
                        request.user.save()
                        team = Team(name=form.cleaned_data["team_name"], season=active_season, user=request.user)
                        team.save()
                        messages.success(request, f'Welcome to {league.abbreviation}')
                        return redirect(reverse('leagues:league', kwargs={'id': league.id}))
                else:
                    messages.error(request, 'Invalid Password')
            else:
                messages.error(request, 'League Not Found')
    else:
        form = LeagueJoinForm()
    return render(request, "leagues/league_join.html", { "form": form })

@login_required(login_url="/users/login/")
def team_settings_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        active_season = league.get_active_season()
        team = request.user.get_active_season_team(active_season)
        team_names = [t.name.lower() for t in active_season.teams.all() if t.name != team.name]
        if request.method == "POST":
            form = TeamForm(request.POST, request.FILES, instance=team)
            if form.is_valid():
                if form.cleaned_data["name"].lower() in team_names:
                    messages.error(request, 'Team Name Already Exists')
                else:
                    form.save()
                    messages.success(request, 'Successful Update')
                return redirect(reverse('leagues:teamSettings', kwargs={'id': league.id}))
        else:
            form = TeamForm(instance=team)
        return render(request, "leagues/team/team_settings.html", { 'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), "form": form, "team": team })
    else:
        return redirect("/")

@login_required(login_url="/users/login/")
def league_pokemon_list_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        page = request.GET.get('page', '1')
        pageSize = request.GET.get('page_size', '10')
        orderBy = request.GET.get('order_by', 'name')
        pokemon = Pokemon.objects.defer('pokemon_type_effectives', 'pokemon_coverage_moves', 'pokemon_special_moves', 'pokemon_moves').filter(season=activeSeason).order_by(orderBy)
        p = Paginator(pokemon, pageSize)
        return render(request, "leagues/pokemon/league_pokemon_list.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason, 'pokemonPage': p.page(page), 'lastPage': p.num_pages, 'pageSize': pageSize, 'orderBy': orderBy})
    else:
        return redirect("/")

@login_required(login_url="/users/login/")
def league_pokemon_tiers_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        tiers = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        return render(request, "leagues/pokemon/league_pokemon_tiers.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason, 'tiers': tiers})
    else:
        return redirect("/")

@login_required(login_url="/users/login/")
def get_tier(request, league_id, tier):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
        activeSeason = league.get_active_season()
        orderBy = request.GET.get('order_by', 'name')
        pokemon = Pokemon.objects.defer('pokemon_type_effectives', 'pokemon_coverage_moves', 'pokemon_special_moves', 'pokemon_moves').filter(season=activeSeason, point_value=tier).order_by(orderBy)
        return render(request, "leagues/pokemon/league_pokemon_tier.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'tier': tier, 'pokemon': pokemon, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)

@login_required(login_url="/users/login/")
def league_pokemon_type_tiers_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        types = Type.objects.all()
        return render(request, "leagues/pokemon/league_pokemon_type_tiers.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason, 'types': types})
    else:
        return redirect("/")

@login_required(login_url="/users/login/")
def get_type_tier(request, league_id, type_id):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
        activeSeason = league.get_active_season()
        orderBy = request.GET.get('order_by', '-point_value')
        pokemon = Pokemon.objects.defer('pokemon_type_effectives', 'pokemon_coverage_moves', 'pokemon_special_moves', 'pokemon_moves').filter(season=activeSeason, point_value__isnull=False, pokemon_types__type__id=type_id).order_by(orderBy)
        type = Type.objects.get(id=type_id)
        return render(request, "leagues/pokemon/league_pokemon_type_tier.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'type': type, 'pokemon': pokemon, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)

@login_required(login_url="/users/login/")
def league_pokemon_search(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        form = PokemonSearchForm()
        return render(request, "leagues/pokemon/league_pokemon_search.html", {'form': form, 'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id)})
    else:
        return HttpResponse(status=400)

@login_required(login_url="/users/login/")
def league_pokemon_search_results(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        page = 1
        pageSize = 10
        orderBy = 'name'
        p = None
        if request.method == "POST":
            orderBy = request.POST.get('order_by', 'name')
            form = PokemonSearchForm(data=request.POST)
            if form.is_valid():
                page = request.GET.get('page', '1')
                pageSize = request.GET.get('page_size', '10')
                orderBy = request.GET.get('order_by', '-point_value')
                pokemon_objects = Pokemon.objects.filter(season=activeSeason)

                for f in form.fields:
                    if f.startswith('base_') and form.cleaned_data[f] is not None:
                        pokemon_objects = pokemon_objects.filter(**{f.split('base_')[1]: form.cleaned_data[f]})
                    if f.startswith('and_') and form.cleaned_data[f] is not None:
                        tokens = list(filter(None, form.cleaned_data[f].split(',')))
                        if len(tokens) > 0:
                            for t in tokens:
                                if '___' in f:
                                    query_tokens = f.split('___')
                                    pokemon_objects = pokemon_objects.filter(Q(**{query_tokens[0].split('and_')[1]: t.strip()}) & Q(**{query_tokens[1]: float(query_tokens[2])}))
                                else:
                                    pokemon_objects = pokemon_objects.filter(**{f.split('and_')[1]: t.strip()})
                    if f.startswith('or') and form.cleaned_data[f] is not None:
                        tokens = list(filter(None, form.cleaned_data[f].split(',')))
                        if len(tokens) > 0:
                            if '___' in f:
                                query_tokens = f.split('___')
                                pokemon_objects = pokemon_objects.filter(functools.reduce(lambda q, t: q | Q(Q(**{query_tokens[0].split('or_')[1]: t.strip()}) & Q(**{query_tokens[1]: float(query_tokens[2])})), tokens, Q()))
                            else:
                                pokemon_objects = pokemon_objects.filter(functools.reduce(lambda q, t: q | Q(**{f.split('or_')[1]: t.strip()}), tokens, Q()))
                pokemon_objects = pokemon_objects.filter(point_value__isnull=False)
                pokemon = pokemon_objects.distinct().order_by(orderBy)
                p = Paginator(pokemon, pageSize)
        else: 
            form = PokemonSearchForm()
        return render(request, "leagues/pokemon/league_pokemon_search_results.html", {'form': form, 'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'pokemonPage': p.page(page) if p is not None else None, 'lastPage': p.num_pages if p is not None else None, 'pageSize': pageSize, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)
    
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
        team_id = request.GET.get('teamId', None)
        return render(request, "leagues/admin/modify_team.html", {'league': league, 'teams': activeSeason.teams.all(), 'isLeagueModerator': request.user.is_league_moderator(league.id), 'teamId': team_id})
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
        form = PokemonSimpleSearchForm()
        return render(request, "leagues/admin/modifiable_team.html", {"form": form, 'league': league, "team": team, "pokemon": team.pokemons.all()})
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
                pokemon_objects = Pokemon.objects.filter(season=activeSeason, team=None, point_value__isnull=False)
                for f in form.fields:
                    pokemon_objects = pokemon_objects.filter(**{f: form.cleaned_data[f]})
                pokemon = pokemon_objects.distinct().order_by('name')[:10]
        else: 
            form = PokemonSimpleSearchForm()
        return render(request, "leagues/admin/simple_search_results.html", {'form': form, 'league': league, "team": team, 'undraftedPokemon': pokemon})
    else:
        return HttpResponse(status=400)