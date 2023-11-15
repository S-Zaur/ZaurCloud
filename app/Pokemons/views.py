import json

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.mail import get_connection, EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect

from Pokemons.API.pokemon_utils import *
from Pokemons.API.views import api_save_pokemon


def index(request):
    if request.method == "POST":
        if request.POST["action"] == "FTP":
            return api_save_pokemon(request, request.POST["name"])
    if "action" in request.GET:
        if request.GET["action"] == "Properties":
            return JsonResponse(get_pokemon(request.GET["name"]).to_json())
        return default_get_actions(request)
    return render(request, 'Pokemons/index.html',
                  context=pokemons_list(get_payload(request), base_page=reverse(index)))


def fight(request):
    if request.method == "POST":
        if "action" not in request.POST:
            raise SuspiciousOperation
        if request.POST["action"] == "Email":
            return send_email(request.user, "PokeFight",
                              f"ваш покемон {request.POST['player_pokemon']} встретился с {request.POST['opponent_pokemon']} в результате боя он {'победил' if request.POST['result'] == 'WIN' else 'проиграл'}")
    if "action" in request.GET:
        if request.GET["action"] == "Hit":
            player_pokemon = Pokemon(**json.loads(request.GET["player_pokemon"].replace("'", '"')))
            opponent_pokemon = Pokemon(**json.loads(request.GET["opponent_pokemon"].replace("'", '"')))
            number = int(request.GET["number"])
            return JsonResponse(fight_hit(player_pokemon, opponent_pokemon, number))
        if request.GET["action"] == "Fast":
            player_pokemon = Pokemon(**json.loads(request.GET["player_pokemon"].replace("'", '"')))
            opponent_pokemon = Pokemon(**json.loads(request.GET["opponent_pokemon"].replace("'", '"')))
            return JsonResponse(fight_fast(player_pokemon, opponent_pokemon))
        return default_get_actions(request)
    return render(request, "Pokemons/fight.html",
                  context=fight_start(request.GET["playerPokemon"], request.GET["opponentPokemon"]))


def default_get_actions(request):
    if request.GET["action"] == "Search":
        try:
            poke = get_pokemon(request.GET["name"])
            return render(request, 'Pokemons/index.html', context={"pokemons": [poke]})
        except Http404:
            return render(request, 'Pokemons/index.html', context={"errors": "not found"}, status=404)
    if request.GET["action"] == "Battle":
        url = reverse('Pokemons.battle')
        player_pokemon = request.GET["name"]
        opponent_pokemon = get_random_pokemon().name
        return redirect(f"{url}?playerPokemon={player_pokemon}&opponentPokemon={opponent_pokemon}")
    raise SuspiciousOperation


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
