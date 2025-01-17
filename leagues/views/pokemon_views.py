from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q

import functools

from leagues.forms import PokemonSearchForm
from leagues.models import League
from pokemons.models import Pokemon, Type, DetailedMove, PokemonAbility

@login_required(login_url="/users/login/")
def league_pokemon_list_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        page = request.GET.get('page', '1')
        pageSize = request.GET.get('page_size', '10')
        orderBy = request.GET.get('order_by', 'name')
        pokemon = Pokemon.objects.defer('pokemon_type_effectives', 'pokemon_detailed_moves', 'pokemon_coverage_moves', 'pokemon_special_moves', 'pokemon_moves').filter(season=activeSeason).order_by(orderBy)
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
        pokemon = Pokemon.objects.defer('pokemon_type_effectives', 'pokemon_detailed_moves', 'pokemon_coverage_moves', 'pokemon_special_moves', 'pokemon_moves').filter(season=activeSeason, point_value=tier).order_by(orderBy)
        return render(request, "leagues/pokemon/league_pokemon_tier.html", {'league': league, 'tier': tier, 'pokemon': pokemon, 'orderBy': orderBy, 'tierListZoom': tierListZoom})
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
        pokemon = Pokemon.objects.defer('pokemon_type_effectives', 'pokemon_detailed_moves', 'pokemon_coverage_moves', 'pokemon_special_moves', 'pokemon_moves').filter(season=activeSeason, point_value__isnull=False, pokemon_types__type__id=type_id).order_by(orderBy)
        type = Type.objects.get(id=type_id)
        return render(request, "leagues/pokemon/league_pokemon_type_tier.html", {'league': league, 'type': type, 'pokemon': pokemon, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)

@login_required(login_url="/users/login/")
def league_pokemon_search(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        move_id = request.GET.get('move_id', None)
        ability_id = request.GET.get('ability_id', None)
        type_id = request.GET.get('type_id', None)
        form = PokemonSearchForm()
        if move_id is not None:
            move = DetailedMove.objects.get(id=move_id)
            form['and_pokemon_detailed_moves__detailed_move__name__iexact'].initial = [move.name.capitalize()]
        if ability_id is not None:
            ability = PokemonAbility.objects.get(id=ability_id)
            form['and_pokemon_abilities__name__iexact'].initial = [ability.name.capitalize()]
        if type_id is not None:
            type = Type.objects.get(id=type_id)
            form['and_pokemon_types__type__name__iexact'].initial = [type.name.capitalize()]
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
        pokemon = Pokemon.objects.prefetch_related('pokemon_detailed_moves__detailed_move__type').get(id=pokemon_id)
        special_move_dict = get_pokemon_special_move_dictionary(pokemon)
        coverage_move_dict = get_pokemon_coverage_move_dictionary(pokemon)
        return render(request, "leagues/pokemon/league_pokemon_modal.html", {'league': league, 'pokemon': pokemon, 'special_move_dict': special_move_dict, 'coverage_move_dict': coverage_move_dict})
    else:
        return HttpResponse(status=400)
    
def get_pokemon_special_move_dictionary(pokemon):
    special_move_dictionary = {}
    special_moves = pokemon.pokemon_detailed_moves.filter(detailed_move__special_category__isnull=False).order_by('detailed_move__special_category', 'detailed_move__type__name', 'detailed_move__name')
    for sm in special_moves:
        move = sm.detailed_move
        if move.special_category not in special_move_dictionary:
            special_move_dictionary[move.special_category] = []
        special_move_dictionary[move.special_category].append({'name': move.name, 'category': move.category, 'color': move.type.color, 'id': move.id})
    return special_move_dictionary

def get_pokemon_coverage_move_dictionary(pokemon):
    coverage_move_dictionary = {}
    coverage_moves = pokemon.pokemon_detailed_moves.filter(detailed_move__viable=True).order_by('detailed_move__type__name', 'detailed_move__category', 'detailed_move__name')
    for cm in coverage_moves:
        move = cm.detailed_move
        if move.type.name not in coverage_move_dictionary:
            coverage_move_dictionary[move.type.name] = []
        coverage_move_dictionary[move.type.name].append({'name': move.name, 'category': move.category, 'color': move.type.color, 'id': move.id})
    return coverage_move_dictionary