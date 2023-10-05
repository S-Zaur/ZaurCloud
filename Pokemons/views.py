import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests as r
from django.utils import timezone
from django.views.decorators.cache import never_cache

from Pokemons.models import Battle, Pokemon
from Pokemons.pokemon_utils import parce_pokemons, get_random_pokemon, get_pokemon, pokemons_battle


def index(request):
    if "action" in request.GET:
        if request.GET["action"] == "Properties":
            return JsonResponse(get_pokemon(request.GET["name"]).__dict__)
        if request.GET["action"] == "Battle":
            return redirect("battle", player_pokemon=request.GET["name"], opponent_pokemon=get_random_pokemon().name)
        if request.GET["action"] == "Search":
            poke = get_pokemon(request.GET["name"])
            return render(request, 'Pokemons/index.html', context={"objects": [poke]})
    payload = {'limit': 100, 'offset': 0}
    if "limit" in request.GET:
        payload['limit'] = request.GET['limit']
    if "offset" in request.GET:
        payload['offset'] = request.GET['offset']
    response = r.get('https://pokeapi.co/api/v2/pokemon', params=payload).json()
    pokemons = parce_pokemons(response['results'])
    return render(request, 'Pokemons/index.html',
                  context={"objects": pokemons, 'next': response['next'].split('?')[1] if response['next'] else None,
                           'prev': response['previous'].split('?')[1] if response['previous'] else None})


@never_cache
def battle(request, player_pokemon, opponent_pokemon):
    if request.method == "POST":
        Battle.objects.create(player_pokemon=request.POST["player_pokemon"],
                              opponent_pokemon=request.POST["opponent_pokemon"],
                              result=request.POST["result"] == "WIN",
                              user=request.user if request.user.is_authenticated else None,
                              battle_date=timezone.localtime())
        return JsonResponse({"result": "ok"})
    if "action" in request.GET:
        if request.GET["action"] == "Hit":
            player_pokemon = Pokemon(**json.loads(request.GET["player_pokemon"]))
            opponent_pokemon = Pokemon(**json.loads(request.GET["opponent_pokemon"]))
            number = int(request.GET["number"])
            return JsonResponse(pokemons_battle(player_pokemon, opponent_pokemon, number))
        if request.GET["action"] == "Search":
            poke = get_pokemon(request.GET["name"])
            return render(request, 'Pokemons/index.html', context={"objects": [poke]})
        if request.GET["action"] == "Battle":
            return redirect("battle", player_pokemon=request.GET["name"], opponent_pokemon=get_random_pokemon().name)
        if request.GET["action"] == "Revenge":
            pass
    return render(request, "Pokemons/battle.html",
                  context={"player": get_pokemon(player_pokemon), "opponent": get_pokemon(opponent_pokemon)})
