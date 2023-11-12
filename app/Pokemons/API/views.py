import datetime
import io
import json
from ftplib import FTP

from django.conf import settings
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
    return JsonResponse(pokemons_list(get_payload(request), base_page=reverse('Pokemons.API.List')))


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


@require_http_methods(["POST", "GET"])
def api_save_pokemon(request, pokemon_id: int):
    pokemon = get_pokemon(pokemon_id)
    with FTP(settings.FTP_SERVER) as ftp:
        ftp.login(user=settings.FTP_USERNAME, passwd=settings.FTP_PASSWORD)
        folder_name = datetime.datetime.today().strftime("%Y%m%d")
        if folder_name not in ftp.nlst():
            ftp.mkd(folder_name)
        result = f"# {pokemon.name}\n "
        result += f"|   Property   | Description |\n| ----------- | ----------- |\n"
        for key in pokemon.__dict__:
            result += f"|{key}|{pokemon.__dict__[key]}|\n"
        bio = io.BytesIO(result.encode('ascii'))
        ftp.storbinary(f'STOR {folder_name}/{pokemon.name}.md', bio)
    return JsonResponse({"result": "ok"})
