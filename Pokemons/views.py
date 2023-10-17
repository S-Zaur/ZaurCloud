import json

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.mail import get_connection, EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache

from Pokemons.models import Pokemon, FightResult
from Pokemons.API.pokemon_utils import get_payload, pokemons_list, get_pokemon, get_random_pokemon, pokemons_battle


def index(request):
    if "action" in request.GET:
        if request.GET["action"] == "Properties":
            return JsonResponse(get_pokemon(request.GET["name"]).to_json())
        if request.GET["action"] == "Battle":
            return redirect(reverse(
                "Pokemons.battle") + "?" + f"playerPokemon={request.GET['name']}&opponentPokemon={get_random_pokemon().name}")
        if request.GET["action"] == "Search":
            poke = get_pokemon(request.GET["name"])
            return render(request, 'Pokemons/index.html', context={"pokemons": [poke]})
    return render(request, 'Pokemons/index.html', context=pokemons_list(get_payload(request), base_page=reverse(index)))


@never_cache
def fight(request):
    if request.method == "POST":
        if "action" not in request.POST:
            raise SuspiciousOperation
        if request.POST["action"] == "Result":
            FightResult.objects.create(player_pokemon=request.POST["player_pokemon"],
                                       opponent_pokemon=request.POST["opponent_pokemon"],
                                       result=request.POST["result"] == "WIN",
                                       user=request.user if request.user.is_authenticated else None,
                                       battle_date=timezone.localtime())
            return JsonResponse({"result": "ok"})
        if request.POST["action"] == "Email":
            return send_email(request.user, "PokeBattle",
                              f"ваш покемон {request.POST['player_pokemon']} встретился с {request.POST['opponent_pokemon']} в результате боя он {'победил' if request.POST['result'] == 'WIN' else 'проиграл'}")
    if "action" in request.GET:
        if request.GET["action"] == "Hit":
            player_pokemon = Pokemon(**json.loads(request.GET["player_pokemon"].replace("'", '"')))
            opponent_pokemon = Pokemon(**json.loads(request.GET["opponent_pokemon"].replace("'", '"')))
            number = int(request.GET["number"])
            return JsonResponse(pokemons_battle(player_pokemon, opponent_pokemon, number))
        if request.GET["action"] == "Search":
            poke = get_pokemon(request.GET["name"])
            return render(request, 'Pokemons/index.html', context={"pokemons": [poke]})
        if request.GET["action"] == "Battle":
            return redirect(reverse(
                "Pokemons.battle") + "?" + f"playerPokemon={request.GET['name']}&opponentPokemon={get_random_pokemon().name}")
        if request.GET["action"] == "Revenge":
            pass
    player_pokemon = request.GET["playerPokemon"]
    opponent_pokemon = request.GET["opponentPokemon"]
    return render(request, "Pokemons/fight.html",
                  context={"player": get_pokemon(player_pokemon), "opponent": get_pokemon(opponent_pokemon)})


def send_email(user, subject, message):
    with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
    ) as connection:
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()

    return JsonResponse({"result": "ok"})
