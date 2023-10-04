from django.http import JsonResponse
from django.shortcuts import render
import requests as r

from Pokemons.pokemon_utils import parce_pokemons, get_pokemon


def index(request):
    if "action" in request.GET:
        if request.GET["action"] == "Properties":
            return JsonResponse(get_pokemon(request.GET["name"]).__dict__)
    if "name" in request.GET:
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
