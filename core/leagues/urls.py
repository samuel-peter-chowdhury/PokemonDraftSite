from django.urls import path
from . import views

app_name = 'leagues'

urlpatterns = [
    path('create/', views.create_view, name="create"),
    path('<int:id>', views.league_view, name="league"),
    path('initialize/season/<int:id>', views.initialize_season_view, name="initializeSeason"),
]