from django.urls import path

from Pokemons import views

urlpatterns = [
    path("", views.index, name="index"),
    path("battle/<str:player_pokemon>/<str:opponent_pokemon>", views.battle, name="battle"),
]
