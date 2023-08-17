from django.urls import path

from . import views

urlpatterns = [
    path("", views.open_dir, name="index"),
    path("<path:path>", views.open_dir, name="open_dir"),
]
