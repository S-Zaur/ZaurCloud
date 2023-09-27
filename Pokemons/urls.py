from django.urls import path

from Pokemons import views

urlpatterns = [
    path("", views.index, name="index"),
]
