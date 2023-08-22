import mimetypes
import os
import shutil
import tempfile
import urllib.parse
import uuid
import zipfile

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from Cloud.models import CloudObject
from Cloud.utils import get_files_and_dirs, check_permissions, check_exists, get_dir_size, get_properties


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
            return delete(file_path)
        if action == "Rename":
            return rename(file_path, request.POST["new_name"])
        if action == "CreateDirectory":
            if "in_place" in request.POST:
                file_path = os.path.join(file_path, "HelloWorld")
            return create_directory(file_path)
        if action == "Upload":
            return upload(file_path, request.FILES)
        raise SuspiciousOperation

    if "action" in request.GET:
        action = request.GET["action"]
        file_path = urllib.parse.unquote(request.GET["url"])
        file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, file_path))
        if action == "Download":
            return download(file_path)
        if action == "Properties":
            return properties(file_path)
        raise SuspiciousOperation

    if os.path.isfile(file_path):
        raise SuspiciousOperation("Cannot open files")
    objects = get_files_and_dirs(file_path)
    obj = CloudObject(file_path)
    return render(request, 'Cloud/cloud.html', context={
        "objects": objects,
        "name": obj.name,
        "url": obj.get_rel_url()
    })


@check_exists
def download(path):
    if os.path.isdir(path):
        if get_dir_size(path) > 1e9:
            return JsonResponse({"result": "Downloadable object too large"}, status=403)
        zip_file_name = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + ".zip")
        with zipfile.ZipFile(zip_file_name, 'w') as zipObj:
            for folderName, subFolders, filenames in os.walk(path):
                for subFolder in subFolders:
                    zipObj.mkdir(subFolder)
                for filename in filenames:
                    file_path = os.path.join(folderName, filename)
                    zipObj.write(file_path, os.path.relpath(file_path, path))
        return download(zip_file_name)
    with open(path, 'rb') as file:
        mime_type, _ = mimetypes.guess_type(path)
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Length'] = os.path.getsize(path)
        response['Content-Disposition'] = "attachment; filename=%s" % os.path.split(path)[-1]
        return response


@check_exists
def delete(path):
    if settings.DEBUG:
        return JsonResponse({"result": "DEBUG"}, status=403)
    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)
    return JsonResponse({"result": "ok"})


@check_exists
def rename(path, name):
    name = os.path.join(os.path.split(path)[0], name)
    os.rename(path, name)
    obj = CloudObject(name)
    return JsonResponse({
        "result": "ok",
        "abs_url": obj.get_absolute_url(),
        "rel_url": obj.get_rel_url(),
        "name": obj.name,
    })


@check_exists
def properties(path):
    return JsonResponse(get_properties(path))


def create_directory(path):
    file_path = os.path.split(path)[0]
    path = os.path.join(file_path, "Новая папка")
    if os.path.exists(path):
        i = 2
        while os.path.exists(path):
            path = os.path.join(file_path, f"Новая папка ({i})")
            i += 1
    os.mkdir(path)
    obj = CloudObject(path)
    return JsonResponse({
        "result": "ok",
        "name": obj.name,
        "img": "/static/" + obj.get_icon(),
        "rel_url": obj.get_rel_url(),
        "abs_url": obj.get_absolute_url(),
    })


def upload(path, files):
    result = {"files": []}
    for filename, file in files.items():
        name = files[filename].name
        file_path = os.path.join(path, name)
        if os.path.exists(file_path):
            result["files"].append({
                "name": name,
                "exists": "true"
            })
            continue
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        obj = CloudObject(file_path)
        result["files"].append({
            "name": obj.name,
            "img": "/static/" + obj.get_icon(),
            "rel_url": obj.get_rel_url(),
        })
    result["result"] = "ok"
    return JsonResponse(result)
