from django.urls import path, include

from Pokemons import views

urlpatterns = [
    path("", views.index, name="Pokemons.index"),
    path('api/', include("Pokemons.API.urls")),
    path("battle/", views.fight, name="Pokemons.battle"),
]
