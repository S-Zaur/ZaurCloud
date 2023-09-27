from django.http import Http404
from django.shortcuts import render
import requests as r
import json


# Create your views here.

def index(request):
    if "name" in request.GET:
        response = r.get('https://pokeapi.co/api/v2/pokemon/' + request.GET["name"])
        if response.status_code == 404:
            raise Http404
        return render(request, 'Pokemons/index.html', context={"poke": True, "result": response.json()})
    payload = {'limit': 100, 'offset': 0}
    response = r.get('https://pokeapi.co/api/v2/pokemon', params=payload)
    return render(request, 'Pokemons/index.html', context={"objects": response.json()})
