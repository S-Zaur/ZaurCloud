import os
import urllib.parse

from django.core.exceptions import SuspiciousOperation
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from Cloud.models import CloudObject, Shared, Favorites
from Cloud.utils import file_manager
from Cloud.utils.core import get_files_and_dirs, check_permissions, parse_url


@check_permissions
def open_dir(request, path=""):
    file_path = parse_url(path)
    if os.path.isfile(file_path):
        raise SuspiciousOperation("Cannot open files")
    objects = get_files_and_dirs(file_path)
    obj = CloudObject(real_path=file_path)
    return render(
        request,
        "Cloud/cloud/index.html",
        context={"objects": objects, "name": obj.name, "url": obj.get_rel_url()},
    )


@check_permissions
def upload(request):
    file_path = parse_url(request.POST["url"])
    return file_manager.upload(file_path, request.FILES)


@check_permissions
def download(request):
    file_path = parse_url(request.GET["url"])
    return file_manager.download(file_path)


@check_permissions
def properties(request):
    file_path = parse_url(request.GET["url"])
    return file_manager.properties(file_path)


@check_permissions
def create_directory(request):
    file_path = parse_url(request.POST["url"])
    if "in-place" in request.POST:
        file_path = os.path.join(file_path, "HelloWorld")
    return file_manager.create_directory(file_path)


@check_permissions
def copy(request):
    file_path = parse_url(request.POST["url"])
    return file_manager.copy(file_path, request.POST["cut"], request.user)


@check_permissions
def paste(request):
    file_path = parse_url(request.POST["url"])
    return file_manager.paste(file_path, request.user)


@check_permissions
def delete(request):
    file_path = parse_url(request.POST["url"])
    return file_manager.delete(file_path)


@check_permissions
def rename(request):
    file_path = parse_url(request.POST["url"])
    new_name = request.POST["new-name"]
    if len(new_name) == 0:
        return JsonResponse({"error": "Имя файла не может быть пустым"}, status=400)
    if new_name[0] == ".":
        return JsonResponse(
            {"error": "Имя файла не может начинаться с '.'"}, status=400
        )
    return file_manager.rename(file_path, request.POST["new-name"])


@check_permissions
def favorites(request):
    objects = CloudObject.objects.filter(favorites__user_id=request.user.id)
    return render(
        request,
        "Cloud/favorites/index.html",
        context={
            "objects": objects,
            "name": "Избранное",
        },
    )


@check_permissions
def add_to_favorites(request):
    file_path = parse_url(request.POST["url"])
    if not os.path.exists(file_path):
        raise Http404
    co, _ = CloudObject.objects.get_or_create(real_path=file_path)
    fv, created = Favorites.objects.get_or_create(obj=co, user=request.user)
    if not created:
        return JsonResponse({"result": "Already added"})
    return JsonResponse({"result": "ok"})


@check_permissions
def remove_from_favorites(request):
    file_path = parse_url(request.POST["url"])
    if not os.path.exists(file_path):
        raise Http404
    (
        Favorites.objects.filter(user_id=request.user.id)
        & Favorites.objects.filter(obj__real_path=file_path)
    ).delete()
    return JsonResponse({"result": "ok"})


@check_permissions
def shared_all(request):
    objects = Shared.objects.filter(parent=None)
    return render(
        request,
        "Cloud/shared/index.html",
        context={
            "objects": objects,
            "name": "Общее",
        },
    )


def shared(request, uuid):
    objects = get_object_or_404(Shared, uuid=uuid)
    if not objects.obj.is_file:
        objects = Shared.objects.filter(parent_id=uuid)
        return render(
            request,
            "Cloud/shared/index.html",
            context={
                "objects": objects,
                "name": CloudObject.objects.get(shared__uuid=uuid).name,
                "uuid": uuid,
            },
        )
    return render(
        request,
        "Cloud/shared/index.html",
        context={"objects": [objects], "name": objects.obj.name, "uuid": uuid},
    )


@check_permissions
def create_shareable_link(request):
    file_path = parse_url(request.POST["url"])
    if not os.path.exists(file_path):
        raise Http404
    co, _ = CloudObject.objects.get_or_create(real_path=file_path)
    res, _ = Shared.objects.get_or_create(obj_id=co.id)
    if co.is_file:
        return JsonResponse(
            {"result": "ok", "url": reverse("Cloud.shared", args=[res.uuid])}
        )
    for addr, dirs, files in os.walk(file_path):
        s = Shared.objects.get(obj__real_path=addr)
        for directory in dirs:
            co, _ = CloudObject.objects.get_or_create(
                real_path=os.path.join(addr, directory)
            )
            Shared.objects.get_or_create(obj=co, parent=s)
        for file in files:
            co, _ = CloudObject.objects.get_or_create(
                real_path=os.path.join(addr, file)
            )
            Shared.objects.get_or_create(obj=co, parent=s)
    return JsonResponse(
        {"result": "ok", "url": reverse("Cloud.shared", args=[res.uuid])}
    )


@check_permissions
def delete_shareable_link(request):
    file_path = parse_url(
        CloudObject.objects.get(shared__uuid=request.POST["uuid"]).path
    )
    Shared.objects.get(obj__real_path=file_path).delete()
    return JsonResponse({"result": "ok"})


@check_permissions
def goto(request):
    if "url" in request.GET:
        path = urllib.parse.unquote(request.GET["url"])
    else:
        path = CloudObject.objects.get(shared__uuid=request.GET["uuid"]).path

    if not os.path.exists(path):
        raise Http404
    url = os.path.split(path)[0]
    if url == "":
        return redirect(reverse("Cloud.index"))
    return redirect(reverse("Cloud.open_dir", args=[url]))
