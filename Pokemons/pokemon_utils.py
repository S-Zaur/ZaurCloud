from django.http import Http404

from Pokemons.models import Pokemon
import requests as r


def parce_pokemons(json):
    pokemons = []
    for poke in json:
        pokemons.append(Pokemon(id=poke['url'].split('/')[-2], name=poke['name']))
    return pokemons


def get_pokemon(name):
    response = r.get('https://pokeapi.co/api/v2/pokemon/' + name)
    if response.status_code == 404:
        raise Http404
    return parce_pokemon(response.json())


def parce_pokemon(json):
    stats = json['stats']
    hp, attack = 0, 0
    for stat in stats:
        if stat["stat"]["name"] == "hp":
            hp = stat["base_stat"]
        if stat["stat"]["name"] == "attack":
            attack = stat["base_stat"]
    return Pokemon(
        id=json['id'],
        name=json['name'],
        is_default=json['is_default'],
        base_experience=json['base_experience'],
        height=json['height'],
        weight=json['weight'],
        species=json['species']['name'],
        hp=hp,
        attack=attack,
    )
