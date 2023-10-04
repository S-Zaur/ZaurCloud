from dataclasses import dataclass

from django.db import models


# Create your models here.
@dataclass
class Pokemon:
    id: int
    name: str
    hp: int = None
    attack: int = None
    is_default: bool = None
    base_experience: int = None
    height: int = None
    weight: int = None
    species: str = None
