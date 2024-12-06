from django.urls import path
from . import views

app_name = 'leagues'

urlpatterns = [
    path('<int:id>', views.league_view, name="league"),
    path('join', views.league_join_view, name="leagueJoin"),
    path('<int:id>/team/settings', views.team_settings_view, name="teamSettings"),
    path('<int:id>/pokemon/list', views.league_pokemon_list_view, name="leaguePokemonList"),
    path('<int:id>/pokemon/tiers', views.league_pokemon_tiers_view, name="leaguePokemonTiers"),
    path('<int:id>/pokemon/type/tiers', views.league_pokemon_type_tiers_view, name="leaguePokemonTypeTiers"),
    path('<int:id>/pokemon/search', views.league_pokemon_search, name="leaguePokemonSearch"),
    path('initialize/season/<int:id>', views.initialize_season_view, name="initializeSeason"),
    path('initialize/point/data/<int:id>', views.initialize_point_data_view, name="initializePointData"),
    path('<int:id>/admin/team', views.modify_team_view, name="adminModifyTeam"),
]

htmx_urlpatterns = [
    path('<int:league_id>/pokemon/tier/<int:tier>', views.get_tier, name="leaguePokemonTier"),
    path('<int:league_id>/pokemon/type/tier/<int:type_id>', views.get_type_tier, name="leaguePokemonTypeTier"),
    path('<int:id>/pokemon/search/results', views.league_pokemon_search_results, name="leaguePokemonSearchResults"),
    path('<int:league_id>/admin/team/<int:team_id>', views.get_modifiable_team_view, name="adminModifiableTeam"),
    path('<int:league_id>/admin/team/<int:team_id>/simple/search/results', views.admin_simple_search_results, name="adminSimpleSearchResults"),
]

urlpatterns += htmx_urlpatterns