from django.http import Http404
from django.shortcuts import render
import requests as r

from Pokemons.models import Pokemon


# Create your views here.

def index(request):
    if "name" in request.GET:
        response = r.get('https://pokeapi.co/api/v2/pokemon/' + request.GET["name"])
        if response.status_code == 404:
            raise Http404
        poke = parce_pokemon(response.json())
        return render(request, 'Pokemons/index.html', context={"poke": poke})
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


def parce_pokemons(json):
    pokemons = []
    for poke in json:
        pokemons.append(Pokemon(id=poke['url'].split('/')[-2], name=poke['name']))
    return pokemons


def parce_pokemon(json):
    return Pokemon(
        id=json['id'],
        name=json['name'],
        is_default=json['is_default'],
        base_experience=json['base_experience'],
        height=json['height'],
        weight=json['weight'],
        species=json['species']['name'],
    )
