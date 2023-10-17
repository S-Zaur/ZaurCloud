import json

from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from Pokemons.API.pokemon_utils import *
from Pokemons.models import Pokemon


def check400(func):
    def wrapper(request, *args, **kwargs):
        if request.method == "GET":
            if "player_pokemon" not in request.GET or "opponent_pokemon" not in request.GET:
                raise SuspiciousOperation
        if request.method == "POST":
            if "player_pokemon" not in request.POST or "opponent_pokemon" not in request.POST:
                raise SuspiciousOperation
        return func(request, *args, **kwargs)

    return wrapper


@require_http_methods(["GET"])
def api_pokemons_list(request):
    return JsonResponse(pokemons_list(get_payload(request)))


@require_http_methods(["GET"])
def api_get_pokemon(request, pokemon_id):
    return JsonResponse({"pokemon": get_pokemon(pokemon_id).to_json()})


@require_http_methods(["GET"])
def api_random_pokemon(request):
    return JsonResponse({"pokemon": get_random_pokemon().to_json()})


@require_http_methods(["GET", "POST"])
@check400
def api_fight(request, number: int = None):
    if request.method == "POST":
        player_pokemon = Pokemon(**json.loads(request.POST["player_pokemon"].replace("'", '"')))
        opponent_pokemon = Pokemon(**json.loads(request.POST["opponent_pokemon"].replace("'", '"')))
        return JsonResponse(fight_hit(player_pokemon, opponent_pokemon, number))
    return JsonResponse(fight_start(request.GET["player_pokemon"], request.GET["opponent_pokemon"]))


@require_http_methods(["GET"])
@check400
def api_fast_fight(request):
    player_pokemon = Pokemon(**json.loads(request.GET["player_pokemon"].replace("'", '"')))
    opponent_pokemon = Pokemon(**json.loads(request.GET["opponent_pokemon"].replace("'", '"')))
    return JsonResponse(fight_fast(player_pokemon, opponent_pokemon))
