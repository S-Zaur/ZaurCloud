import os
import urllib.parse

from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from Cloud.models import CloudObject, Shared
from Cloud.utils import favorites_manager
from Cloud.utils import file_manager
from Cloud.utils import share_manager
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
        if action == "Share":
            return share_manager.share(file_path)
        if action == "Copy":
            return file_manager.copy(file_path, request.POST["cut"], request.user)
        if action == "Paste":
            return file_manager.paste(file_path, request.user)
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
        return redirect(reverse("Cloud.open_dir", args=[url]))
    file_path = parse_url(url)
    if action == "Download":
        return file_manager.download(file_path)
    if action == "Properties":
        return file_manager.properties(file_path)
    raise SuspiciousOperation


@check_permissions
def shared_all(request):
    if request.method == "POST" or "action" in request.GET:
        return shared_actions(request)
    objects = Shared.objects.filter(parent=None)
    return render(request, 'Cloud/shared/index.html', context={
        "objects": objects,
        "name": "Общее",
    })


def shared(request, uuid):
    if request.method == "POST" or "action" in request.GET:
        return shared_actions(request)
    objects = get_object_or_404(Shared, uuid=uuid)
    if not objects.obj.is_file:
        objects = Shared.objects.filter(parent_id=uuid)
        return render(request, 'Cloud/shared/index.html', context={
            "objects": objects,
            "name": CloudObject.objects.get(shared__uuid=uuid).name,
            "uuid": uuid
        })
    return render(request, 'Cloud/shared/index.html', context={
        "objects": [objects],
        "name": objects.obj.name,
        "uuid": uuid
    })


def shared_actions(request):
    if request.method == "POST":
        if "action" not in request.POST:
            raise SuspiciousOperation
        action = request.POST["action"]
        file_path = parse_url(CloudObject.objects.get(shared__uuid=request.POST["uuid"]).path)
        if action == "Unshare":
            return share_manager.unshare(file_path)
        raise SuspiciousOperation
    if "action" in request.GET:
        return default_get_actions(request.GET["action"],
                                   CloudObject.objects.get(shared__uuid=request.GET["uuid"]).path)
