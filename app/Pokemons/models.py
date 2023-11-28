from dataclasses import dataclass, asdict

from django.conf import settings
from django.db import models


@dataclass
class Pokemon:
    id: int
    name: str
    hp: int = None
    attack: int = None
    defense: int = None
    base_experience: int = None
    height: int = None
    weight: int = None
    species: str = None

    def __str__(self):
        return self.name

    def to_json(self):
        return asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})


class FightResult(models.Model):
    player_pokemon = models.TextField()
    opponent_pokemon = models.TextField()
    result = models.BooleanField()
    rounds_count = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    battle_date = models.DateTimeField()
