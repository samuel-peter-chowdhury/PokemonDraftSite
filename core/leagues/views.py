from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

from .forms import LeagueCreationForm
from .models import League

# Create your views here.
@user_passes_test(lambda u: u.is_superuser)
def create_view(request):
    if request.method == "POST":
        form = LeagueCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else: 
        form = LeagueCreationForm()
    return render(request, "leagues/create.html", { "form": form })

def league_view(request, id):
    if request.user.has_league(id):
        league = League.objects.get(id=id)
        return render(request, "leagues/league.html", {'league': league})
    else:
        return redirect("/")