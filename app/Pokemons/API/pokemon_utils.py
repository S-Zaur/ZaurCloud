import random

import requests as r
from django.core.cache import cache
from django.http import Http404
from django.urls import reverse
from django.utils import timezone

from Pokemons.models import Pokemon, FightResult


def get_payload(request):
    payload = {'limit': 100, 'offset': 0}
    if "limit" in request.GET:
        payload['limit'] = request.GET['limit']
    if "offset" in request.GET:
        payload['offset'] = request.GET['offset']
    return payload


def pokemons_list(payload, base_page=None):
    sentinel = object()
    result = cache.get((str(payload) + base_page).replace(' ', '_'), sentinel)
    if result is not sentinel:
        return result
    response = r.get('https://pokeapi.co/api/v2/pokemon', params=payload).json()
    if base_page is None:
        base_page = reverse("Pokemons.API.List")
    next_page = base_page + "?" + response["next"].split("?")[1] if response["next"] is not None else None
    prev_page = base_page + "?" + response["previous"].split("?")[1] if response["previous"] is not None else None
    result = {"count": int(response["count"]),
              "next": next_page,
              "prev": prev_page,
              "pokemons": parce_pokemons(response['results'])}
    cache.set((str(payload) + base_page).replace(' ', '_'), result)
    return result


def get_pokemon(pokemon_id):
    sentinel = object()
    result = cache.get(str(pokemon_id), sentinel)
    if result is not sentinel:
        return result
    response = r.get('https://pokeapi.co/api/v2/pokemon/' + str(pokemon_id))
    if response.status_code == 404:
        raise Http404
    result = parce_pokemon(response.json())
    cache.set(str(pokemon_id), result)
    return result


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


def fight_hit(request, player_pokemon: Pokemon, opponent_pokemon: Pokemon, user_number: int):
    rnd = random.randint(1, 10)
    if (user_number % 2) == (rnd % 2):
        description = hit(player_pokemon, opponent_pokemon)
    else:
        description = hit(opponent_pokemon, player_pokemon)
    if player_pokemon.hp == 0 or opponent_pokemon.hp == 0:
        FightResult.objects.create(player_pokemon=player_pokemon.name,
                                   opponent_pokemon=opponent_pokemon.name,
                                   result=opponent_pokemon.hp == 0,
                                   battle_date=timezone.localtime(),
                                   user=request.user if request.user.is_authenticated else None)
    return {
        "player_pokemon": player_pokemon.to_json(),
        "opponent_pokemon": opponent_pokemon.to_json(),
        "description": description
    }


def hit(first_pokemon: Pokemon, second_pokemon: Pokemon):
    damage = int(max(first_pokemon.attack - second_pokemon.defense * (random.random() * 0.3 + 0.65), 0))
    damage = damage if damage > 0 else random.randint(1, 10)
    second_pokemon.hp = max(second_pokemon.hp - damage, 0)
    return f"{first_pokemon.name} бьет {second_pokemon.name} и наносит {damage} урона"


def fight_start(player_pokemon, opponent_pokemon):
    return {"player_pokemon": get_pokemon(player_pokemon).to_json(),
            "opponent_pokemon": get_pokemon(opponent_pokemon).to_json()}


def fight_fast(request, player_pokemon: Pokemon, opponent_pokemon: Pokemon):
    description_list = []
    while player_pokemon.hp > 0 and opponent_pokemon.hp > 0:
        if (random.randint(1, 10) % 2) == (random.randint(1, 10) % 2):
            description_list.append({"description": hit(player_pokemon, opponent_pokemon)})
        else:
            description_list.append({"description": hit(opponent_pokemon, player_pokemon)})
    FightResult.objects.create(player_pokemon=player_pokemon.name,
                               opponent_pokemon=opponent_pokemon.name,
                               result=opponent_pokemon.hp == 0,
                               battle_date=timezone.localtime(),
                               user=request.user if request.user.is_authenticated else None)
    return {
        "player_pokemon": player_pokemon.to_json(),
        "opponent_pokemon": opponent_pokemon.to_json(),
        "description_list": description_list
    }
