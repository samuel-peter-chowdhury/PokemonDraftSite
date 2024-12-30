from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from pokemons.models import Pokemon

@login_required(login_url="/users/login/")
def homepage(request):
    leagues = request.user.get_all_leagues()
    if len(leagues) > 0:
        return redirect(reverse('leagues:leaguePokemonTiers', kwargs={'id': leagues[0].id}))
    else:
        return redirect(reverse('leagues:leagueJoin'))