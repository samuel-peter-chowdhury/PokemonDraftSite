from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q

import functools

from leagues.forms import PokemonSearchForm
from leagues.models import League
from pokemons.models import Pokemon, Type, Move, Ability

@login_required(login_url="/users/login/")
def league_pokemon_list_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        page = request.GET.get('page', '1')
        pageSize = request.GET.get('page_size', '10')
        orderBy = request.GET.get('order_by', 'name')
        pokemon = Pokemon.objects.defer('type_effectives', 'moves', 'abilities').filter(season=activeSeason).order_by(orderBy)
        p = Paginator(pokemon, pageSize)
        return render(request, "leagues/pokemon/league_pokemon_list.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason, 'pokemonPage': p.page(page), 'lastPage': p.num_pages, 'pageSize': pageSize, 'orderBy': orderBy})
    else:
        return redirect("/")

@login_required(login_url="/users/login/")
def league_pokemon_tiers_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        tiers = reversed(range(1, activeSeason.max_tier_value + 1))

        tierListZoom = request.GET.get('tier_list_zoom', None)
        if tierListZoom:
            request.session['tier_list_zoom'] = tierListZoom
        else:
            tierListZoom = request.session.get('tier_list_zoom', 'compact')

        return render(request, "leagues/pokemon/league_pokemon_tiers.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason, 'tiers': tiers, 'tierListZoom': tierListZoom})
    else:
        return redirect("/")

@login_required(login_url="/users/login/")
def get_tier(request, league_id, tier):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
        activeSeason = league.get_active_season()
        orderBy = request.GET.get('order_by', 'name')
        tierListZoom = request.GET.get('tier_list_zoom', 'compact')
        pokemon = Pokemon.objects.defer('type_effectives', 'moves', 'abilities').filter(season=activeSeason, point_value=tier).order_by(orderBy)
        return render(request, "leagues/pokemon/league_pokemon_tier.html", {'league': league, 'tier': tier, 'pokemon': pokemon, 'orderBy': orderBy, 'tierListZoom': tierListZoom})
    else:
        return HttpResponse(status=400)

@login_required(login_url="/users/login/")
def league_pokemon_type_tiers_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        types = [choice[0] for choice in Type.choices]
        return render(request, "leagues/pokemon/league_pokemon_type_tiers.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason, 'types': types})
    else:
        return redirect("/")

@login_required(login_url="/users/login/")
def get_type_tier(request, league_id):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
        activeSeason = league.get_active_season()
        type = request.GET.get('type', None)
        orderBy = request.GET.get('order_by', '-point_value')
        pokemon = Pokemon.objects.defer('type_effectives', 'moves', 'abilities').filter(season=activeSeason, point_value__isnull=False, types__contains=type).order_by(orderBy)
        return render(request, "leagues/pokemon/league_pokemon_type_tier.html", {'league': league, 'type': type, 'pokemon': pokemon, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)

@login_required(login_url="/users/login/")
def league_pokemon_search(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        move_id = request.GET.get('move_id', None)
        ability_id = request.GET.get('ability_id', None)
        type = request.GET.get('type', None)
        form = PokemonSearchForm()
        if move_id is not None:
            move = Move.objects.get(id=move_id)
            form['and_moves__name__iexact'].initial = [move.name.capitalize()]
        if ability_id is not None:
            ability = Ability.objects.get(id=ability_id)
            form['and_abilities__name__iexact'].initial = [ability.name.capitalize()]
        if type is not None:
            form['and_types__icontains'].initial = [type]
        return render(request, "leagues/pokemon/league_pokemon_search.html", {'form': form, 'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id)})
    else:
        return HttpResponse(status=400)

@login_required(login_url="/users/login/")
def league_pokemon_search_results(request, league_id):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
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
                    if f.startswith('exclude_') and form.cleaned_data[f] is not None and form.cleaned_data[f]:
                        pokemon_objects = pokemon_objects.filter(team=None)
                    if f.startswith('base_') and form.cleaned_data[f] is not None:
                        pokemon_objects = pokemon_objects.filter(**{f.split('base_', 1)[1]: form.cleaned_data[f]})
                    if f.startswith('and_') and form.cleaned_data[f] is not None:
                        tokens = list(filter(None, form.cleaned_data[f]))
                        if len(tokens) > 0:
                            for t in tokens:
                                if '___' in f:
                                    query_tokens = f.split('___')
                                    pokemon_objects = pokemon_objects.filter(Q(**{query_tokens[0].split('and_')[1]: t.strip()}) & Q(**{query_tokens[1]: float(query_tokens[2])}))
                                else:
                                    pokemon_objects = pokemon_objects.filter(**{f.split('and_')[1]: t.strip()})
                    if f.startswith('or_') and form.cleaned_data[f] is not None:
                        tokens = list(filter(None, form.cleaned_data[f]))
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
        return render(request, "leagues/pokemon/league_pokemon_search_results.html", {'form': form, 'league': league, 'pokemonPage': p.page(page) if p is not None else None, 'lastPage': p.num_pages if p is not None else None, 'pageSize': pageSize, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)
    
@login_required(login_url="/users/login/")
def get_pokemon_modal(request, league_id, pokemon_id):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
        pokemon = Pokemon.objects.get(id=pokemon_id)
        special_move_dict = get_pokemon_special_move_dictionary(pokemon)
        coverage_move_dict = get_pokemon_coverage_move_dictionary(pokemon)
        return render(request, "leagues/pokemon/league_pokemon_modal.html", {'league': league, 'pokemon': pokemon, 'special_move_dict': special_move_dict, 'coverage_move_dict': coverage_move_dict})
    else:
        return HttpResponse(status=400)
    
def get_pokemon_special_move_dictionary(pokemon):
    special_move_dictionary = {}
    special_moves = pokemon.moves.filter(special_categories__isnull=False).order_by('special_categories', 'type', 'name')
    for sm in special_moves:
        for c in sm.get_special_categories():
            if c not in special_move_dictionary:
                special_move_dictionary[c] = []
            special_move_dictionary[c].append({'name': sm.name, 'category': sm.category, 'type': sm.type, 'id': sm.id, 'description': sm.description})
    return special_move_dictionary

def get_pokemon_coverage_move_dictionary(pokemon):
    coverage_move_dictionary = {}
    coverage_moves = pokemon.moves.filter(viable=True).order_by('type', 'category', 'name')
    for cm in coverage_moves:
        if cm.type not in coverage_move_dictionary:
            coverage_move_dictionary[cm.type] = []
        tooltip = f'Power: {cm.base_power}  |  Accuracy: {cm.accuracy}  |  {cm.description}'
        coverage_move_dictionary[cm.type].append({'name': cm.name, 'category': cm.category, 'type': cm.type, 'id': cm.id, 'tooltip': tooltip})
    return coverage_move_dictionary