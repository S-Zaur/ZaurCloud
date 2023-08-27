from django.urls import path

from . import views

urlpatterns = [
    path("", views.open_dir, name="index"),
    path("favorites", views.favorites, name="favorites"),
    path("shared/all", views.shared_all, name="shared_all"),
    path("shared/<uuid:uuid>", views.shared, name="shared"),
    path("<path:path>", views.open_dir, name="open_dir"),
]
