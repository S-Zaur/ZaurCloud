import random
from django.http import Http404
from django.urls import reverse
from Pokemons.models import Pokemon
import requests as r


def get_payload(request):
    payload = {'limit': 100, 'offset': 0}
    if "limit" in request.GET:
        payload['limit'] = request.GET['limit']
    if "offset" in request.GET:
        payload['offset'] = request.GET['offset']
    return payload


def pokemons_list(payload, base_page=None):
    response = r.get('https://pokeapi.co/api/v2/pokemon', params=payload).json()
    if base_page is None:
        base_page = reverse("Pokemons.API.List")
    next_page = base_page + "?" + response["next"].split("?")[1] if response["next"] is not None else None
    prev_page = base_page + "?" + response["previous"].split("?")[1] if response["previous"] is not None else None
    return {"count": int(response["count"]),
            "next": next_page,
            "prev": prev_page,
            "pokemons": parce_pokemons(response['results'])}


def get_pokemon(pokemon_id):
    response = r.get('https://pokeapi.co/api/v2/pokemon/' + str(pokemon_id))
    if response.status_code == 404:
        raise Http404
    return parce_pokemon(response.json())


def get_random_pokemon():
    response = r.get('https://pokeapi.co/api/v2/pokemon', params={"limit": 1, "offset": 0}).json()
    response = r.get('https://pokeapi.co/api/v2/pokemon', params={"limit": response["count"], "offset": 0}).json()
    pokemon = response["results"][random.randint(0, response["count"])]
    response = r.get('https://pokeapi.co/api/v2/pokemon/' + pokemon["name"])
    return parce_pokemon(response.json())


def parce_pokemons(json):
    pokemons = []
    for poke in json:
        pokemons.append(Pokemon(id=poke['url'].split('/')[-2], name=poke['name']).to_json())
    return pokemons


def parce_pokemon(json):
    stats = json['stats']
    hp, attack, defense = 0, 0, 0
    for stat in stats:
        if stat["stat"]["name"] == "hp":
            hp = stat["base_stat"]
        if stat["stat"]["name"] == "attack":
            attack = stat["base_stat"]
        if stat["stat"]["name"] == "defense":
            defense = stat["base_stat"]
    return Pokemon(
        id=json['id'],
        name=json['name'],
        base_experience=json['base_experience'],
        height=json['height'],
        weight=json['weight'],
        species=json['species']['name'],
        hp=hp,
        attack=attack,
        defense=defense,
    )


def pokemons_battle(first_pokemon, second_pokemon, user_number):
    rnd = random.randint(1, 10)
    if (user_number % 2) == (rnd % 2):
        damage = int(max(first_pokemon.attack - second_pokemon.defense * (random.random() * 0.3 + 0.65), 0))
        damage = damage if damage > 0 else random.randint(1, 10)
        second_pokemon.hp = max(second_pokemon.hp - damage, 0)
        return {"opponent_pokemon": second_pokemon.__dict__,
                "description": f"{first_pokemon.name} бьет {second_pokemon.name} " f"и наносит {damage} урона"}
    else:
        damage = int(max(second_pokemon.attack - first_pokemon.defense * (random.random() * 0.3 + 0.65), 0))
        damage = damage if damage > 0 else random.randint(1, 10)
        first_pokemon.hp = max(first_pokemon.hp - damage, 0)
        return {"player_pokemon": first_pokemon.__dict__,
                "description": f"{second_pokemon.name} бьет {first_pokemon.name} " f"и наносит {damage} урона"}
