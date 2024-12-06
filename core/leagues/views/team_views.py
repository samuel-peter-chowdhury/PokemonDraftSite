from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from leagues.models import League
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