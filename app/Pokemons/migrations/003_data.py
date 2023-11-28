import random
from datetime import timedelta

import requests as r
from django.db import migrations
from django.utils import timezone


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def generate_data(apps, schema_editor):
    FightResult = apps.get_model("Pokemons", "FightResult")
    d1 = timezone.localtime()
    d2 = timezone.localtime() - timedelta(days=30)
    response = r.get('https://pokeapi.co/api/v2/pokemon', params={"limit": 1, "offset": 0}).json()
    response = r.get('https://pokeapi.co/api/v2/pokemon', params={"limit": response["count"], "offset": 0}).json()
    for i in range(random.randint(700, 1300)):
        pokemon1 = response["results"][random.randint(0, response["count"] // 10)]["name"]
        pokemon2 = response["results"][random.randint(0, response["count"] // 10)]["name"]
        FightResult.objects.create(player_pokemon=pokemon1,
                                   opponent_pokemon=pokemon2,
                                   result=random.random() > 0.5,
                                   battle_date=random_date(d2, d1),
                                   rounds_count=random.randint(1, 10),
                                   user=None)


class Migration(migrations.Migration):
    dependencies = [
        ('Pokemons', '0002_fightresult_rounds_count'),
    ]

    operations = [
        migrations.RunPython(generate_data),
    ]
