import mimetypes
import os
import shutil
import tempfile
import uuid
import zipfile

from django.conf import settings
from django.core.cache import cache
from django.http import Http404, HttpResponse, JsonResponse
from django.utils.encoding import escape_uri_path

from Cloud.models import CloudObject
from Cloud.utils.core import check_exists, get_dir_size, get_properties


def archive(path):
    zip_file_name = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + ".zip")
    with zipfile.ZipFile(zip_file_name, 'w') as zipObj:
        for folderName, subFolders, filenames in os.walk(path):
            for subFolder in subFolders:
                zipObj.mkdir(subFolder)
            for filename in filenames:
                file_path = os.path.join(folderName, filename)
                zipObj.write(file_path, os.path.relpath(file_path, path))
    return zip_file_name


@check_exists
def download(path):
    if os.path.isdir(path):
        if get_dir_size(path) > 1e9:
            return JsonResponse({"error": "Скачиваемая папка слишком большая"}, status=403)
        return download(archive(path))
    with open(path, 'rb') as file:
        mime_type, _ = mimetypes.guess_type(path)
        mime_type = "application/octet-stream" if mime_type is None else mime_type
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Length'] = os.path.getsize(path)
        response['Content-Disposition'] = "attachment; filename=" + escape_uri_path(os.path.split(path)[-1])
        return response


@check_exists
def delete(path):
    CloudObject.objects.filter(real_path=path).delete()
    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)
    return JsonResponse({"result": "ok"})


@check_exists
def rename(path, name):
    name = os.path.join(os.path.split(path)[0], name)
    os.rename(path, name)
    obj = CloudObject.objects.filter(real_path=path).first()
    if obj:
        obj.real_path = name
        obj.path = name.replace(settings.STORAGE_DIRECTORY + "/", "").replace('\\', '/')
        obj.name = os.path.split(name)[1]
        obj.ext = os.path.splitext(name)[1][1:].lower()
        obj.save()
    obj = CloudObject(real_path=name)
    return JsonResponse({
        "result": "ok",
        "abs_url": obj.get_absolute_url(),
        "rel_url": obj.get_rel_url(),
        "name": obj.name,
    })


@check_exists
def properties(path):
    return JsonResponse(get_properties(path))


def get_unique_name(path, name):
    if not os.path.exists(os.path.join(path, name)):
        return name
    i = 2
    name, ext = os.path.splitext(name)
    new_path = os.path.join(path, f"{name} ({i}){ext}")
    while os.path.exists(new_path):
        i += 1
        new_path = os.path.join(path, f"{name} ({i}){ext}")
    return f"{name} ({i}){ext}"


def create_directory(path):
    file_path = os.path.split(path)[0]
    if not os.path.exists(file_path):
        raise Http404
    path = os.path.join(file_path, get_unique_name(file_path, "Новая папка"))
    os.mkdir(path)
    obj = CloudObject(real_path=path)
    return JsonResponse({
        "result": "ok",
        "name": obj.name,
        "img": "/static/" + obj.get_icon(),
        "rel_url": obj.get_rel_url(),
        "abs_url": obj.get_absolute_url(),
    })

@check_exists
def upload(path, files):
    result = {"files": []}
    for filename, file in files.items():
        name = files[filename].name
        file_path = os.path.join(path, get_unique_name(path, name))
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        obj = CloudObject(real_path=file_path)
        result["files"].append({
            "name": obj.name,
            "img": "/static/" + obj.get_icon(),
            "rel_url": obj.get_rel_url(),
        })
    result["result"] = "ok"
    return JsonResponse(result)


@check_exists
def copy(path, cut, user):
    cache.set(user.id, {"files": [CloudObject(real_path=path)], "cut": cut})
    return JsonResponse({"result": "ok"})


@check_exists
def paste(path, user):
    sentinel = object()
    cb = cache.get(user.id, sentinel)
    if cb is sentinel:
        return JsonResponse({"result": "ok", "files": []})
    result = {"files": []}
    for obj in cb["files"]:
        obj.name = get_unique_name(path, obj.name)
        if obj.is_file:
            new_path = shutil.copy2(obj.real_path, os.path.join(path, obj.name))
        else:
            new_path = shutil.copytree(obj.real_path, os.path.join(path, obj.name))
        co = CloudObject(real_path=new_path)
        result["files"].append({
            "name": co.name,
            "img": "/static/" + co.get_icon(),
            "rel_url": co.get_rel_url(),
            "abs_url": co.get_absolute_url() if not co.is_file else None
        })
        if cb["cut"] == "True":
            delete(obj.real_path)
    result["result"] = "ok"
    return JsonResponse(result)
