from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q

import json
import csv

from leagues.forms import PokemonSimpleSearchForm, DataUploadForm, SubmitMatchupForm
from leagues.models import League, Team, Week, Matchup, Game
#from leagues.data import initialize_all_pokemon_data, initialize_pokemon_data, initialize_point_value_data, initialize_schedule_data, export_pokemon_data
from pokemons.models import Pokemon, GameStat
from users.models import CustomUser

# @user_passes_test(lambda u: u.is_superuser)
# def initialize_schedule_data_view(request, id):
#     league = League.objects.get(id=id)
#     activeSeason = league.get_active_season()
#     if request.method == "POST":
#         form = DataUploadForm(request.POST, request.FILES)
#         if form.is_valid() and activeSeason:
#             file = request.FILES['file']
#             decoded_file = file.read().decode('utf-8').splitlines()
#             csv_file = csv.reader(decoded_file)
#             initialize_schedule_data(csv_file, activeSeason)
#     else:
#         form = DataUploadForm()
#     return render(request, "leagues/admin/initialize_schedule_data.html", { "form": form, 'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id) })

# @user_passes_test(lambda u: u.is_superuser)
# def initialize_detailed_move_data_view(request, id):
#     league = League.objects.get(id=id)
#     activeSeason = league.get_active_season()
#     initialize_all_pokemon_data(activeSeason)
#     return render(request, "leagues/admin/initialize_detailed_move_data.html", { 'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id) })

# @user_passes_test(lambda u: u.is_superuser)
# def initialize_pokemon_data_view(request, id):
#     league = League.objects.get(id=id)
#     activeSeason = league.get_active_season()
#     if request.method == "POST":
#         form = DataUploadForm(request.POST, request.FILES)
#         if form.is_valid() and activeSeason:
#             file = request.FILES['file']
#             data = json.load(file)
#             initialize_pokemon_data(data, activeSeason)
#     else:
#         form = DataUploadForm()
#     return render(request, "leagues/admin/initialize_pokemon_data.html", { "form": form, 'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id) })

# @user_passes_test(lambda u: u.is_superuser)
# def initialize_point_data_view(request, id):
#     league = League.objects.get(id=id)
#     activeSeason = league.get_active_season()
#     if request.method == "POST":
#         form = DataUploadForm(request.POST, request.FILES)
#         if form.is_valid() and activeSeason:
#             file = request.FILES['file']
#             decoded_file = file.read().decode('utf-8').splitlines()
#             tsv_file = csv.reader(decoded_file, delimiter="\t")
#             initialize_point_value_data(tsv_file, activeSeason)
#     else:
#         form = DataUploadForm()
#     return render(request, "leagues/admin/initialize_point_data.html", { "form": form, 'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id) })

@login_required(login_url="/users/login/")
def modify_team_view(request, id):
    if request.user.has_league(id) and request.user.is_league_moderator(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        return render(request, "leagues/admin/modify_team.html", {'league': league, 'teams': activeSeason.teams.filter(is_active=True), 'isLeagueModerator': request.user.is_league_moderator(league.id)})
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
        pokemon = team.pokemons.all()
        total_points = sum([p.point_value for p in pokemon])
        form = PokemonSimpleSearchForm()
        return render(request, "leagues/admin/modifiable_team.html", {"form": form, 'league': league, "team": team, "pokemon": pokemon, "totalPoints": total_points})
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
                pokemon_objects = Pokemon.objects.filter(season=activeSeason, point_value__isnull=False)
                for f in form.fields:
                    pokemon_objects = pokemon_objects.filter(**{f: form.cleaned_data[f]})
                pokemon = pokemon_objects.distinct().order_by('name')[:10]
        else: 
            form = PokemonSimpleSearchForm()
        return render(request, "leagues/admin/simple_search_results.html", {'form': form, 'league': league, "team": team, 'undraftedPokemon': pokemon})
    else:
        return HttpResponse(status=400)
    
@login_required(login_url="/users/login/")
def admin_modify_tiers_view(request, id):
    if request.user.has_league(id) and request.user.is_league_moderator(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        tiers = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        return render(request, "leagues/admin/modify_tiers.html", {'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id), 'activeSeason': activeSeason, 'tiers': tiers})
    else:
        return redirect("/")

@login_required(login_url="/users/login/")
def get_admin_modify_tier(request, league_id, tier):
    if request.user.has_league(league_id) and request.user.is_league_moderator(league_id):
        if request.method == "POST":
            pokemon_id = request.GET.get('pokemonId', None)
            point_value = request.POST['point_value']
            p = Pokemon.objects.get(id=pokemon_id)
            p.point_value = point_value
            p.save()
        league = League.objects.get(id=league_id)
        activeSeason = league.get_active_season()
        orderBy = request.GET.get('order_by', 'name')
        pokemon = Pokemon.objects.defer('type_effectives', 'moves', 'abilities').filter(season=activeSeason, point_value=tier).order_by(orderBy)
        return render(request, "leagues/admin/modify_tier.html", {'league': league, 'tier': tier, 'pokemon': pokemon, 'orderBy': orderBy})
    else:
        return HttpResponse(status=400)
    
class PorygonPokemonLine:
    def __init__(self, line):
        self.pokemon = line.split(' has ')[0].strip().lower()
        self.direct_kills = int(line.split(' has ')[1].split('direct kills')[0].strip())
        self.passive_kills = int(line.split('direct kills,')[1].split('passive kills')[0].strip())
        self.deaths = int(line.split('passive kills, and')[1].split('deaths')[0].strip())
        self.pokemon_model = None

    def valid_check(self, team):
        try:
            self.pokemon_model = Pokemon.objects.get(name__icontains=self.pokemon, team=team)
        except:
            raise Exception(f'Pokemon does not exist on the team {team.name}: {self.pokemon}')
        if not ((self.direct_kills >= 0 and self.direct_kills <= 6) and (self.passive_kills >= 0 and self.passive_kills <= 6) and (self.deaths == 0 or self.deaths == 1)):
            raise Exception(f'Pokemon stats are invalid: Direct Kills {self.direct_kills}, Passive Kills {self.passive_kills}, Deaths {self.deaths}')
        

class PorygonOutput:
    def __init__(self, output, active_season):
        self.active_season = active_season
        output_tokens = output.split('||')
        self.winner = output_tokens[1].split(' won ')[0].strip()
        self.differential = int(output_tokens[1].split(' won ')[1].split('-')[0].strip())
        self.coach_one = output_tokens[2].split('**:')[0].split('**')[1].strip()
        self.coach_one_model = None
        self.coach_one_pokemon = []
        for line in output_tokens[3].split('.'):
            line = line.strip()
            if line != '':
                self.coach_one_pokemon.append(PorygonPokemonLine(line.strip()))
        self.coach_two = output_tokens[4].split('**:')[0].split('**')[1].strip()
        self.coach_two_model = None
        self.coach_two_pokemon = []
        for line in output_tokens[5].split('.'):
            line = line.strip()
            if line != '':
                self.coach_two_pokemon.append(PorygonPokemonLine(line.strip()))
        self.replay_link = output_tokens[6].split('**Replay: **')[1].split('**')[0].replace('<', '').replace('>', '').strip()

        self.team_one = None
        self.team_two = None
        self.winning_team = None
        self.losing_team = None

    def valid_check(self):
        try:
            self.coach_one_model = CustomUser.objects.get(showdown_username__iexact=self.coach_one)
            self.team_one = self.coach_one_model.get_active_season_team(self.active_season)
        except:
            raise Exception(f'User with showdown username does not exist: {self.coach_one}')
        try:
            self.coach_two_model = CustomUser.objects.get(showdown_username__iexact=self.coach_two)
            self.team_two = self.coach_two_model.get_active_season_team(self.active_season)
        except:
            raise Exception(f'User with showdown username does not exist: {self.coach_two}')
        if 'https://replay.pokemonshowdown.com/' not in self.replay_link:
            raise Exception(f'Invalid replay link: {self.replay_link}')
        if not (self.winner == self.coach_one or self.winner == self.coach_two):
            raise Exception(f'Winner does not match usernames in body')
        if self.differential > 6 or self.differential < 0:
            raise Exception(f'Differential is invalid: {self.differential}')
        for p in self.coach_one_pokemon:
            p.valid_check(self.team_one)
        for p in self.coach_two_pokemon:
            p.valid_check(self.team_two)
        if self.winner == self.coach_one:
            self.winning_team = self.team_one
            self.losing_team = self.team_two
        else:
            self.winning_team = self.team_two
            self.losing_team = self.team_one
        

class MatchupValidator:
    def __init__(self, week, active_season):
        self.active_season = active_season
        self.week = Week.objects.get(name__iexact=week)
        self.games = []
        self.coaches = []
        self.winner_map = {}
        self.replay_links = []
        self.team_one = None
        self.team_two = None
        self.matchup = None

        self.winning_team = None
        self.losing_team = None

    def valid_check(self):
        if len(self.games) > 0:
            self.coaches.append(self.games[0].coach_one)
            self.coaches.append(self.games[0].coach_two)
            for g in self.games:
                g.valid_check()
                if g.replay_link in self.replay_links:
                    raise Exception(f'Repeated replay link: {g.replay_link}')
                else:
                    self.replay_links.append(g.replay_link)
                if g.coach_one not in self.coaches or g.coach_two not in self.coaches:
                    raise Exception(f'Showdown usernames do not match between games')
                if g.winner in self.winner_map:
                    self.winner_map[g.winner] += 1
                else:
                    self.winner_map[g.winner] = 1
            try:
                self.team_one = self.games[0].team_one
                self.team_two = self.games[0].team_two
                self.matchup = self.week.matchups.get(Q(Q(coach_one=self.team_one) & Q(coach_two=self.team_two)) | Q(Q(coach_one=self.team_two) & Q(coach_two=self.team_one)))
            except:
                raise Exception('Matchup between these players does not exist in this week')
            
            if self.games[0].coach_one in self.winner_map and self.games[0].coach_two in self.winner_map and self.winner_map[self.games[0].coach_one] == self.winner_map[self.games[0].coach_two]:
                raise Exception('No winner can be determined')
            
            winner = max(self.winner_map, key=self.winner_map.get)
            if winner == self.games[0].coach_one:
                self.winning_team = self.team_one
                self.losing_team = self.team_two
            else:
                self.winning_team = self.team_two
                self.losing_team = self.team_one
        else:
            raise Exception('No games in form')

@login_required(login_url="/users/login/")
def submit_matchup_view(request, id):
    if request.user.has_league(id) and request.user.is_league_moderator(id):
        league = League.objects.get(id=id)
        activeSeason = league.get_active_season()
        if request.method == "POST":
            form = SubmitMatchupForm(request.POST)
            if form.is_valid() and activeSeason:
                try:
                    matchupValidator = MatchupValidator(form.cleaned_data['week'], activeSeason)
                    try:
                        matchupValidator.games.append(PorygonOutput(form.cleaned_data['game_one'], activeSeason))
                        matchupValidator.games.append(PorygonOutput(form.cleaned_data['game_two'], activeSeason))
                        game_three = form.cleaned_data['game_three']
                        if game_three is not None and game_three != '':
                            matchupValidator.games.append(PorygonOutput(game_three, activeSeason))
                    except:
                        raise Exception('Could not parse Porygon Output')
                    matchupValidator.valid_check()

                    matchupValidator.matchup.games.all().delete()
                    matchupValidator.matchup.winner = matchupValidator.winning_team
                    matchupValidator.matchup.loser = matchupValidator.losing_team
                    matchupValidator.matchup.save()

                    for g in matchupValidator.games:
                        game = Game()
                        game.matchup = matchupValidator.matchup
                        game.winner = g.winning_team
                        game.loser = g.losing_team
                        game.differential = g.differential
                        game.replay_link = g.replay_link
                        game.save()

                        for p in g.coach_one_pokemon:
                            game_stat = GameStat()
                            game_stat.game = game
                            game_stat.pokemon = p.pokemon_model
                            game_stat.direct_kills = p.direct_kills
                            game_stat.indirect_kills = p.passive_kills
                            game_stat.deaths = p.deaths
                            game_stat.save()

                        for p in g.coach_two_pokemon:
                            game_stat = GameStat()
                            game_stat.game = game
                            game_stat.pokemon = p.pokemon_model
                            game_stat.direct_kills = p.direct_kills
                            game_stat.indirect_kills = p.passive_kills
                            game_stat.deaths = p.deaths
                            game_stat.save()

                    messages.success(request, 'Successfully submitted matchup')
                    form = SubmitMatchupForm()
                except Exception as e:
                    messages.error(request, e)
        else:
            form = SubmitMatchupForm()
        return render(request, "leagues/admin/submit_matchup.html", { "form": form, 'league': league, 'isLeagueModerator': request.user.is_league_moderator(league.id) })
    else:
        return HttpResponse(status=400)