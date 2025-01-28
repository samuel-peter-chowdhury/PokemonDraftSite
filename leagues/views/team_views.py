from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from leagues.models import League, Team
from leagues.forms import TeamForm

from pokemons.models import Type, SpecialMoveCategory, Move

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
def team_matchup_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()

        user_team_id = request.GET.get('userTeamId', None)
        if user_team_id:
            user_team = Team.objects.get(id=user_team_id)
            request.session['team_matchup_user_team_id'] = user_team_id
        else:
            session_user_team_id = request.session.get('team_matchup_user_team_id', None)
            if session_user_team_id:
                user_team = Team.objects.get(id=session_user_team_id)
            else:
                user_team = request.user.get_active_season_team(activeSeason)
                request.session['team_matchup_user_team_id'] = user_team.id
        
        opponent_team_id = request.GET.get('opponentTeamId', None)
        if opponent_team_id:
            opponent_team = Team.objects.get(id=opponent_team_id)
            request.session['team_matchup_opponent_team_id'] = opponent_team_id
        else:
            session_opponent_team_id = request.session.get('team_matchup_opponent_team_id', None)
            if session_opponent_team_id:
                opponent_team = Team.objects.get(id=session_opponent_team_id)
            else:
                opponent_team = None

        return render(request, "leagues/team/team_matchup.html", {'league': league, 'teams': activeSeason.teams.filter(is_active=True), 'isLeagueModerator': request.user.is_league_moderator(league.id),
                                                                  'userTeam': user_team, 'opponentTeam': opponent_team})
    else:
        return redirect("/")
    
@login_required(login_url="/users/login/")
def speed_tier_matchup(request, league_id):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
        orderBy = request.GET.get('order_by', '-speed')
        teams = []

        user_team_id = request.GET.get('user_team_id', request.user.id)
        userTeam = Team.objects.get(id=user_team_id)
        userPokemon = userTeam.pokemons.order_by(orderBy)
        teams.append({'team': userTeam, 'pokemon': userPokemon, 'colors': {'header': '#279ff0', 'sprite': '#62bfff', 'row': '#a9d9f7,#cdebfc'}})

        opponent_team_id = request.GET.get('opponent_team_id', None)
        if opponent_team_id is not None and opponent_team_id != '':
            opponentTeam = Team.objects.get(id=opponent_team_id)
            opponentPokemon = opponentTeam.pokemons.order_by(orderBy)
            teams.append({'team': opponentTeam, 'pokemon': opponentPokemon, 'colors': {'header': '#ea4637', 'sprite': '#ff7c7b', 'row': '#febebd,#ffd3d1'}})
        return render(request, "leagues/team/speed_tier_matchup.html", {'league': league, 'teams': teams, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)
    
@login_required(login_url="/users/login/")
def team_table(request, league_id, team_id):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
        orderBy = request.GET.get('order_by', '-point_value')
        team = Team.objects.get(id=team_id)
        pokemon = team.pokemons.order_by(orderBy)
        return render(request, "leagues/team/team_table.html", {'league': league, 'team': team, 'pokemon': pokemon, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)
    
@login_required(login_url="/users/login/")
def type_effective(request, league_id, team_id):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
        team = Team.objects.get(id=team_id)
        pokemon = team.pokemons.order_by('-point_value')
        types = [choice[0] for choice in Type.choices]
        totalTypeEffectiveMap = {}
        for p in pokemon:
            for pte in p.type_effectives.all():
                if pte.type not in totalTypeEffectiveMap:
                    totalTypeEffectiveMap[pte.type] = 0
                if pte.value == 0:
                    totalTypeEffectiveMap[pte.type] += 1.5 * get_type_effective_weight(p.point_value)
                elif pte.value == 0.25:
                    totalTypeEffectiveMap[pte.type] += 1.25 * get_type_effective_weight(p.point_value)
                elif pte.value == 0.5:
                    totalTypeEffectiveMap[pte.type] += 1 * get_type_effective_weight(p.point_value)
                elif pte.value == 1:
                    pass
                elif pte.value == 2:
                    totalTypeEffectiveMap[pte.type] += -1 * get_type_effective_weight(p.point_value)
                elif pte.value == 4:
                    totalTypeEffectiveMap[pte.type] += -1.25 * get_type_effective_weight(p.point_value)
        orderedTypeEffective = []
        for t in types:
            orderedTypeEffective.append({'type': t, 'total': totalTypeEffectiveMap[t]})
        orderedTypeEffective = sorted(orderedTypeEffective, key = lambda x: (x['total']), reverse=True)
        return render(request, "leagues/team/type_effective.html", {'league': league, 'team': team, 'pokemon': pokemon, 'types': types, 'totalTypeEffective': totalTypeEffectiveMap, 'orderedTypeEffective': orderedTypeEffective})
    else:
        return HttpResponse(status=400)
    
def get_type_effective_weight(point_value):
    if (point_value <= 20 and point_value >= 16):
        return 4
    elif (point_value <= 15 and point_value >= 11):
        return 3
    elif (point_value <= 10 and point_value >= 6):
        return 2
    else:
        return 1
    
@login_required(login_url="/users/login/")
def special_moves(request, league_id, team_id):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
        team = Team.objects.get(id=team_id)
        pokemon = team.pokemons.order_by('-point_value')
        categories = [choice[0] for choice in SpecialMoveCategory.choices]
        specialMoves = {}
        for p in pokemon:
            special_moves = p.moves.filter(special_categories__isnull=False)
            for sm in special_moves:
                for c in sm.get_special_categories():
                    if c not in specialMoves:
                        specialMoves[c] = []
                    specialMoves[c].append({'pokemon': p, 'move': sm.name, 'type': sm.type})
        return render(request, "leagues/team/special_moves.html", {'league': league, 'team': team, 'categories': categories, 'specialMoves': specialMoves})
    else:
        return HttpResponse(status=400)
    
@login_required(login_url="/users/login/")
def team_standings_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        teamStandings = []
        for t in activeSeason.teams.filter(is_active=True):
            match_win_count = t.winner_matchups.all().count()
            match_loss_count = t.loser_matchups.all().count()
            total_match_count = match_win_count + match_loss_count
            match_win_percentage = round((match_win_count / total_match_count) * 100) if total_match_count > 0 else 0
            game_wins = t.winner_games.all()
            game_win_count = game_wins.count()
            game_losses = t.loser_games.all()
            game_loss_count = game_losses.count()
            total_game_count = game_win_count + game_loss_count
            game_win_percentage = round((game_win_count / total_game_count) * 100) if total_game_count > 0 else 0
            pokemon_differential = 0
            for g in game_wins:
                pokemon_differential += g.differential
            for g in game_losses:
                pokemon_differential -= g.differential
            teamStandings.append({'team_name': t.name, 'match_win_count': match_win_count, 'match_loss_count': match_loss_count, 'match_win_percentage': match_win_percentage, 'game_win_count': game_win_count, 'game_loss_count': game_loss_count, 'game_win_percentage': game_win_percentage, 'pokemon_differential': pokemon_differential})
        teamStandings = sorted(teamStandings, key = lambda x: (-x['match_win_percentage'], -x['game_win_percentage'], -x['pokemon_differential']))
        return render(request, "leagues/team/team_standings.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason, 'teamStandings': teamStandings})
    else:
        return redirect("/")