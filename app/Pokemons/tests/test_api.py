import datetime
import random
from ftplib import FTP
from io import BytesIO

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from Pokemons.models import FightResult


class MyTestCase(TestCase):
    def setUp(self):
        self.ok = {"result": "ok"}
        self.pokemons = [{"id": "10274", "name": "ogerpon-hearthflame-mask"},
                         {"id": "10275", "name": "ogerpon-cornerstone-mask"}]
        self.bulbasaur = {
            "pokemon": {"id": 1, "name": "bulbasaur", "hp": 45, "attack": 49, "defense": 49, "base_experience": 64,
                        "height": 7, "weight": 69, "species": "bulbasaur"}}
        self.houndoom = {
            "pokemon": {"id": 229, "name": "houndoom", "hp": 75, "attack": 90, "defense": 50, "base_experience": 175,
                        "height": 14, "weight": 350, "species": "houndoom"}}
        self.bulbasaurmd = b'# bulbasaur\n |   Property   | Description |\n| ----------- | ----------- |\n|id|1|\n|name|bulbasaur|\n|hp|45|\n|attack|49|\n|defense|49|\n|base_experience|64|\n|height|7|\n|weight|69|\n|species|bulbasaur|\n'
        self.fight = {'player_pokemon': {'id': 3, 'name': 'venusaur', 'hp': 80, 'attack': 82, 'defense': 83,
                                         'base_experience': 263, 'height': 20, 'weight': 1000, 'species': 'venusaur'},
                      'opponent_pokemon': {'id': 4, 'name': 'charmander', 'hp': 39, 'attack': 52, 'defense': 43,
                                           'base_experience': 62, 'height': 6, 'weight': 85, 'species': 'charmander'}}
        self.fight_log = [{'player_pokemon': {'id': 3, 'name': 'venusaur', 'hp': 75, 'attack': 82, 'defense': 83,
                                              'base_experience': 263, 'height': 20, 'weight': 1000,
                                              'species': 'venusaur'},
                           'opponent_pokemon': {'id': 4, 'name': 'charmander', 'hp': 39, 'attack': 52, 'defense': 43,
                                                'base_experience': 62, 'height': 6, 'weight': 85,
                                                'species': 'charmander'},
                           'description': 'charmander бьет venusaur и наносит 5 урона'},
                          {'player_pokemon': {'id': 3, 'name': 'venusaur', 'hp': 73, 'attack': 82, 'defense': 83,
                                              'base_experience': 263, 'height': 20, 'weight': 1000,
                                              'species': 'venusaur'},
                           'opponent_pokemon': {'id': 4, 'name': 'charmander', 'hp': 39, 'attack': 52, 'defense': 43,
                                                'base_experience': 62, 'height': 6, 'weight': 85,
                                                'species': 'charmander'},
                           'description': 'charmander бьет venusaur и наносит 2 урона'},
                          {'player_pokemon': {'id': 3, 'name': 'venusaur', 'hp': 73, 'attack': 82, 'defense': 83,
                                              'base_experience': 263, 'height': 20, 'weight': 1000,
                                              'species': 'venusaur'},
                           'opponent_pokemon': {'id': 4, 'name': 'charmander', 'hp': 0, 'attack': 52, 'defense': 43,
                                                'base_experience': 62, 'height': 6, 'weight': 85,
                                                'species': 'charmander'},
                           'description': 'venusaur бьет charmander и наносит 52 урона'},
                          ]
        self.fast_fight_log = {'player_pokemon': {'id': 3, 'name': 'venusaur', 'hp': 67, 'attack': 82, 'defense': 83,
                                                  'base_experience': 263, 'height': 20, 'weight': 1000,
                                                  'species': 'venusaur'},
                               'opponent_pokemon': {'id': 4, 'name': 'charmander', 'hp': 0, 'attack': 52, 'defense': 43,
                                                    'base_experience': 62, 'height': 6, 'weight': 85,
                                                    'species': 'charmander'},
                               'description_list': [{'description': 'charmander бьет venusaur и наносит 4 урона'},
                                                    {'description': 'charmander бьет venusaur и наносит 9 урона'},
                                                    {'description': 'venusaur бьет charmander и наносит 48 урона'}]}

    def test_pokemons_list(self):
        response = self.client.get(reverse('Pokemons.API.List'))
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['count'], 1292)
        self.assertEqual(len(response_json['pokemons']), 100)
        self.assertIsNone(response_json['prev'])
        self.assertEqual(response_json['next'], '/pokemons/api/pokemon/list/?offset=100&limit=100')
        response = self.client.get(reverse('Pokemons.API.List') + "?offset=1290&limit=100")
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['count'], 1292)
        self.assertEqual(response_json['pokemons'], self.pokemons)
        self.assertIsNone(response_json['next'])
        self.assertEqual(response_json['prev'], '/pokemons/api/pokemon/list/?offset=1190&limit=100')

    def test_get_pokemon(self):
        response = self.client.get(reverse('Pokemons.API.GetPokemon', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.bulbasaur)
        response = self.client.get(reverse('Pokemons.API.GetPokemon', args=[42000]))
        self.assertEqual(response.status_code, 404)

    def test_random_pokemon(self):
        random.seed(42)
        response = self.client.get(reverse('Pokemons.API.RandomPokemon'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.houndoom)

    def test_fight(self):
        random.seed(42)
        response = self.client.get(reverse('Pokemons.API.Fight') + "?player_pokemon=3&opponent_pokemon=4")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.fight)
        self.fight['player_pokemon'] = str(self.fight['player_pokemon'])
        self.fight['opponent_pokemon'] = str(self.fight['opponent_pokemon'])
        for f in self.fight_log:
            response = self.client.post(reverse('Pokemons.API.FightInput', args=[1]), self.fight)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), f)
            self.fight['player_pokemon'] = str(response.json()['player_pokemon'])
            self.fight['opponent_pokemon'] = str(response.json()['opponent_pokemon'])
        res = FightResult.objects.all().first()
        self.assertEqual(FightResult.objects.all().count(), 1)
        self.assertEqual(res.player_pokemon, 'venusaur')
        self.assertEqual(res.opponent_pokemon, 'charmander')
        self.assertTrue(res.result)

    def test_fast_fight(self):
        random.seed(42)
        response = self.client.get(reverse('Pokemons.API.Fight') + "?player_pokemon=3&opponent_pokemon=4")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.fight)
        self.fight['player_pokemon'] = str(self.fight['player_pokemon'])
        self.fight['opponent_pokemon'] = str(self.fight['opponent_pokemon'])
        response = self.client.get(reverse('Pokemons.API.FastFight'), self.fight)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.fast_fight_log)
        res = FightResult.objects.all().first()
        self.assertEqual(FightResult.objects.all().count(), 1)
        self.assertEqual(res.player_pokemon, 'venusaur')
        self.assertEqual(res.opponent_pokemon, 'charmander')
        self.assertTrue(res.result)
