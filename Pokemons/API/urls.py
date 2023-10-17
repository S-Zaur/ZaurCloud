from django.urls import path

from Pokemons.API import views

urlpatterns = [
    path("pokemon/list/", views.api_pokemons_list, name="Pokemons.API.List"),
    path("pokemon/<int:pokemon_id>/", views.api_get_pokemon, name="Pokemons.API.GetPokemon"),
    path("pokemon/random/", views.api_random_pokemon, name="Pokemons.API.RandomPokemon"),
    path("fight/", views.api_fight, name="Pokemons.API.Fight"),
    path("fight/<int:number>/", views.api_fight, name="Pokemons.API.FightInput"),
    path("fight/fast/", views.api_fast_fight, name="Pokemons.API.FastFight"),
]
