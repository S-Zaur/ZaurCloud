from django.urls import path

from . import views

urlpatterns = [
    path("", views.open_dir, name="Cloud.index"),
    path("upload/", views.upload, name="Cloud.upload"),
    path("download/", views.download, name="Cloud.download"),
    path("properties/", views.properties, name="Cloud.properties"),
    path("create-ditectory/", views.create_directory, name="Cloud.create_directory"),
    path("copy/", views.copy, name="Cloud.copy"),
    path("paste/", views.paste, name="Cloud.paste"),
    path("delete/", views.delete, name="Cloud.delete"),
    path("rename/", views.rename, name="Cloud.rename"),
    path("favorites", views.favorites, name="Cloud.favorites"),
    path("add-favorite/", views.add_to_favorites, name="Cloud.add_favorite"),
    path("remove-favorite/", views.remove_from_favorites, name="Cloud.remove_favorite"),
    path("shared/all", views.shared_all, name="Cloud.shared_all"),
    path("shared/<uuid:uuid>", views.shared, name="Cloud.shared"),
    path("create-link/", views.create_shareable_link, name="Cloud.create_link"),
    path("delete-link/", views.delete_shareable_link, name="Cloud.delete_link"),
    path("goto/", views.goto, name="Cloud.goto"),
    path("<path:path>", views.open_dir, name="Cloud.open_dir"),
]
