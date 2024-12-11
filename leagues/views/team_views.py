from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from leagues.models import League, Team
from leagues.forms import TeamForm

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

        return render(request, "leagues/team/team_matchup.html", {'league': league, 'teams': activeSeason.teams.all(), 'isLeagueModerator': request.user.is_league_moderator(league.id),
                                                                  'userTeam': user_team, 'opponentTeam': opponent_team})
    else:
        return redirect("/")
    
@login_required(login_url="/users/login/")
def speed_tier_matchup(request, league_id, user_team_id, opponent_team_id):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
        orderBy = request.GET.get('order_by', '-speed')
        userTeam = Team.objects.get(id=user_team_id)
        userPokemon = userTeam.pokemons.order_by(orderBy)
        opponentTeam = Team.objects.get(id=opponent_team_id)
        opponentPokemon = opponentTeam.pokemons.order_by(orderBy)
        return render(request, "leagues/team/speed_tier_matchup.html", {'league': league, 'userTeam': userTeam, 'opponentTeam': opponentTeam, 'userPokemon': userPokemon, 'opponentPokemon': opponentPokemon, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)
    
@login_required(login_url="/users/login/")
def team_table(request, league_id, team_id):
    if request.user.has_league(league_id):
        league = League.objects.get(id=league_id)
        orderBy = request.GET.get('order_by', '-speed')
        team = Team.objects.get(id=team_id)
        pokemon = team.pokemons.order_by(orderBy)
        return render(request, "leagues/team/team_table.html", {'league': league, 'team': team, 'pokemon': pokemon, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)