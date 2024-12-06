from django.urls import path
from .views import base_views, pokemon_views, team_views, admin_views

app_name = 'leagues'

urlpatterns = [
    path('<int:id>', base_views.league_view, name="league"),
    path('join', base_views.league_join_view, name="leagueJoin"),
]

pokemon_urlpatterns = [
    # Standard Paths
    path('<int:id>/pokemon/list', pokemon_views.league_pokemon_list_view, name="leaguePokemonList"),
    path('<int:id>/pokemon/tiers', pokemon_views.league_pokemon_tiers_view, name="leaguePokemonTiers"),
    path('<int:id>/pokemon/type/tiers', pokemon_views.league_pokemon_type_tiers_view, name="leaguePokemonTypeTiers"),
    path('<int:id>/pokemon/search', pokemon_views.league_pokemon_search, name="leaguePokemonSearch"),

    # HTMX Paths
    path('<int:league_id>/pokemon/tier/<int:tier>', pokemon_views.get_tier, name="leaguePokemonTier"),
    path('<int:league_id>/pokemon/type/tier/<int:type_id>', pokemon_views.get_type_tier, name="leaguePokemonTypeTier"),
    path('<int:league_id>/pokemon/search/results', pokemon_views.league_pokemon_search_results, name="leaguePokemonSearchResults"),
]
urlpatterns += pokemon_urlpatterns

team_urlpatterns = [
    path('<int:id>/team/settings', team_views.team_settings_view, name="teamSettings"),
]
urlpatterns += team_urlpatterns

admin_urlpatterns = [
    # Data Initialization Paths
    path('initialize/season/<int:id>', admin_views.initialize_season_view, name="initializeSeason"),
    path('initialize/point/data/<int:id>', admin_views.initialize_point_data_view, name="initializePointData"),

    # Standard Paths
    path('<int:id>/admin/team', admin_views.modify_team_view, name="adminModifyTeam"),

    # HTMX Paths
    path('<int:league_id>/admin/team/<int:team_id>', admin_views.get_modifiable_team_view, name="adminModifiableTeam"),
    path('<int:league_id>/admin/team/<int:team_id>/simple/search/results', admin_views.admin_simple_search_results, name="adminSimpleSearchResults"),
]
urlpatterns += admin_urlpatterns