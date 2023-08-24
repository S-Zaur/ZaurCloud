import os
import urllib.parse

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render, redirect
from django.urls import reverse

import Cloud.utils.favorites_manager as fav_m
import Cloud.utils.file_manager as fm
from Cloud.models import CloudObject
from Cloud.utils.core import get_files_and_dirs, check_permissions


@check_permissions
def open_dir(request, path=""):
    file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, path))
    if request.method == "POST":
        if "action" not in request.POST:
            raise SuspiciousOperation
        action = request.POST["action"]
        file_path = urllib.parse.unquote(request.POST["url"])
        file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, file_path))
        if action == "Delete":
            return fm.delete(file_path)
        if action == "Rename":
            return fm.rename(file_path, request.POST["new-name"])
        if action == "CreateDirectory":
            if "in-place" in request.POST:
                file_path = os.path.join(file_path, "HelloWorld")
            return fm.create_directory(file_path)
        if action == "Upload":
            return fm.upload(file_path, request.FILES)
        if action == "AddFav":
            return fav_m.add_favorite(file_path, request.user)

        raise SuspiciousOperation

    if "action" in request.GET:
        action = request.GET["action"]
        file_path = urllib.parse.unquote(request.GET["url"])
        file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, file_path))
        if action == "Download":
            return fm.download(file_path)
        if action == "Properties":
            return fm.properties(file_path)
        raise SuspiciousOperation

    if os.path.isfile(file_path):
        raise SuspiciousOperation("Cannot open files")
    objects = get_files_and_dirs(file_path)
    obj = CloudObject(path=file_path)
    return render(request, 'Cloud/cloud/index.html', context={
        "objects": objects,
        "name": obj.name,
        "url": obj.get_rel_url()
    })


@check_permissions
def favorites(request):
    if request.method == "POST":
        if "action" not in request.POST:
            raise SuspiciousOperation
        action = request.POST["action"]
        file_path = urllib.parse.unquote(request.POST["url"])
        file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, file_path))
        if action == "DeleteFav":
            return fav_m.delete_favorite(file_path, request.user)
        raise SuspiciousOperation
    if "action" in request.GET:
        action = request.GET["action"]
        if action == "GoTo":
            url = urllib.parse.unquote(request.GET["url"])
            url = os.path.split(url)[0][1:]
            return redirect(reverse("open_dir", args=[url]))
        file_path = urllib.parse.unquote(request.GET["url"])
        file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, file_path))
        if action == "Download":
            return fm.download(file_path)
        if action == "Properties":
            return fm.properties(file_path)
        raise SuspiciousOperation
    objects = CloudObject.objects.filter(
        favorites__user_id=request.user.id
    )
    return render(request, 'Cloud/favorites/index.html', context={
        "objects": objects,
        "name": "Избранное",
    })
