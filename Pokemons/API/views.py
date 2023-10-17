from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from Pokemons.API.pokemon_utils import pokemons_list, get_payload, get_pokemon, get_random_pokemon


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
def fight(request, number: int = None):
    pass


@require_http_methods(["GET"])
def fast_fight(request):
    pass
