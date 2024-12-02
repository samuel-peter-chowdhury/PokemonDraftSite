from django.urls import path
from . import views

app_name = 'leagues'

urlpatterns = [
    path('create/', views.create_view, name="create"),
    path('<int:id>', views.league_view, name="league"),
    path('<int:id>/pokemon/list', views.league_pokemon_list_view, name="leaguePokemonList"),
    path('<int:id>/pokemon/tiers', views.league_pokemon_tiers_view, name="leaguePokemonTiers"),
    path('initialize/season/<int:id>', views.initialize_season_view, name="initializeSeason"),
    path('initialize/point/data/<int:id>', views.initialize_point_data_view, name="initializePointData"),
]

htmx_urlpatterns = [
    path('<int:league_id>/pokemon/tier/<int:tier>', views.get_tier, name="leaguePokemonTier"),
]

urlpatterns += htmx_urlpatterns