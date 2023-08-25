import os
import urllib.parse

from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render, redirect
from django.urls import reverse

from Cloud.models import CloudObject
from Cloud.utils import favorites_manager
from Cloud.utils import file_manager
from Cloud.utils.core import get_files_and_dirs, check_permissions, parse_url


@check_permissions
def open_dir(request, path=""):
    if request.method == "POST":
        if "action" not in request.POST:
            raise SuspiciousOperation
        action = request.POST["action"]
        file_path = parse_url(request.POST["url"])
        if action == "Delete":
            return file_manager.delete(file_path)
        if action == "Rename":
            return file_manager.rename(file_path, request.POST["new-name"])
        if action == "CreateDirectory":
            if "in-place" in request.POST:
                file_path = os.path.join(file_path, "HelloWorld")
            return file_manager.create_directory(file_path)
        if action == "Upload":
            return file_manager.upload(file_path, request.FILES)
        if action == "AddFav":
            return favorites_manager.add_favorite(file_path, request.user)

        raise SuspiciousOperation

    if "action" in request.GET:
        return default_get_actions(request.GET["action"], request.GET["url"])

    file_path = parse_url(path)
    if os.path.isfile(file_path):
        raise SuspiciousOperation("Cannot open files")
    objects = get_files_and_dirs(file_path)
    obj = CloudObject(real_path=file_path)
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
        file_path = parse_url(request.POST["url"])
        if action == "DeleteFav":
            return favorites_manager.delete_favorite(file_path, request.user)
        raise SuspiciousOperation

    if "action" in request.GET:
        return default_get_actions(request.GET["action"], request.GET["url"])

    objects = CloudObject.objects.filter(
        favorites__user_id=request.user.id
    )
    return render(request, 'Cloud/favorites/index.html', context={
        "objects": objects,
        "name": "Избранное",
    })


def default_get_actions(action, url):
    if action == "GoTo":
        url = os.path.split(urllib.parse.unquote(url))[0]
        return redirect(reverse("open_dir", args=[url]))
    file_path = parse_url(url)
    if action == "Download":
        return file_manager.download(file_path)
    if action == "Properties":
        return file_manager.properties(file_path)
    raise SuspiciousOperation
