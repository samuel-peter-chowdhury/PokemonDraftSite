from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from leagues.models import League, Team
from leagues.forms import LeagueJoinForm

@login_required(login_url="/users/login/")
def league_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        return render(request, "leagues/league.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason})
    return redirect(reverse('users:settings'))

@login_required(login_url="/users/login/")
def league_rules_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        return render(request, "leagues/league_rules.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason})
    return redirect(reverse('users:settings'))

@login_required(login_url="/users/login/")
def league_rosters_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        userTeam = request.user.get_active_season_team(activeSeason)
        teams = list(activeSeason.teams.filter(is_active=True).exclude(id=userTeam.id).order_by('name'))
        teams.insert(0, userTeam)
        return render(request, "leagues/league_rosters.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason, 'teams': teams})
    return redirect(reverse('users:settings'))

@login_required(login_url="/users/login/")
def league_schedule_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        weeks = activeSeason.weeks.all().order_by('order')
        return render(request, "leagues/league_schedule.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason, 'weeks': weeks})
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