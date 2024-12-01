from django.urls import path
from . import views

app_name = 'leagues'

urlpatterns = [
    path('create/', views.create_view, name="create"),
]