from django.urls import path

from . import views

urlpatterns = [
    path("", views.open_dir, name="Cloud.index"),
    path("favorites", views.favorites, name="Cloud.favorites"),
    path("shared/all", views.shared_all, name="Cloud.shared_all"),
    path("shared/<uuid:uuid>", views.shared, name="Cloud.shared"),
    path("<path:path>", views.open_dir, name="Cloud.open_dir"),
]
