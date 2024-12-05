from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from pokemons.models import Pokemon

@login_required(login_url="/users/login/")
def homepage(request):
    leagues = request.user.member_leagues.all()
    if len(leagues) > 0:
        return redirect(reverse('leagues:league', kwargs={'id': leagues[0].id}))
    else:
        return redirect(reverse('users:settings'))